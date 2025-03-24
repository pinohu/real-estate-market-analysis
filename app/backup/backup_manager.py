"""
Backup and recovery management system.
"""

import os
import shutil
import logging
import subprocess
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path
import json
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class BackupManager:
    """Manages database and file backups"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.backup_dir = Path(config['BACKUP_DIR'])
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize S3 client if configured
        if config.get('USE_S3_BACKUP'):
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=config['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY'],
                region_name=config['AWS_REGION']
            )
            self.s3_bucket = config['S3_BACKUP_BUCKET']
    
    def create_backup(self, backup_type: str = 'full') -> Dict[str, Any]:
        """Create a backup of the specified type"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_info = {
            'timestamp': timestamp,
            'type': backup_type,
            'status': 'success',
            'files': []
        }
        
        try:
            # Create backup directory
            backup_path = self.backup_dir / f"backup_{timestamp}"
            backup_path.mkdir()
            
            # Backup database
            if backup_type in ['full', 'database']:
                self._backup_database(backup_path, backup_info)
            
            # Backup files
            if backup_type in ['full', 'files']:
                self._backup_files(backup_path, backup_info)
            
            # Upload to S3 if configured
            if self.config.get('USE_S3_BACKUP'):
                self._upload_to_s3(backup_path, timestamp)
            
            # Clean up old backups
            self._cleanup_old_backups()
            
            return backup_info
            
        except Exception as e:
            logger.error(f"Backup failed: {str(e)}", exc_info=True)
            backup_info['status'] = 'failed'
            backup_info['error'] = str(e)
            return backup_info
    
    def _backup_database(self, backup_path: Path, backup_info: Dict[str, Any]):
        """Backup the database"""
        db_config = self.config['DATABASE']
        dump_file = backup_path / 'database.sql'
        
        # Create database dump
        cmd = [
            'pg_dump',
            '-h', db_config['host'],
            '-U', db_config['user'],
            '-d', db_config['database'],
            '-f', str(dump_file)
        ]
        
        if db_config.get('password'):
            os.environ['PGPASSWORD'] = db_config['password']
        
        try:
            subprocess.run(cmd, check=True)
            backup_info['files'].append('database.sql')
        finally:
            if db_config.get('password'):
                del os.environ['PGPASSWORD']
    
    def _backup_files(self, backup_path: Path, backup_info: Dict[str, Any]):
        """Backup application files"""
        # Backup uploads
        uploads_dir = Path(self.config['UPLOAD_FOLDER'])
        if uploads_dir.exists():
            shutil.copytree(uploads_dir, backup_path / 'uploads')
            backup_info['files'].append('uploads')
        
        # Backup reports
        reports_dir = Path(self.config['REPORT_FOLDER'])
        if reports_dir.exists():
            shutil.copytree(reports_dir, backup_path / 'reports')
            backup_info['files'].append('reports')
        
        # Backup configuration
        config_file = backup_path / 'config.json'
        with open(config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        backup_info['files'].append('config.json')
    
    def _upload_to_s3(self, backup_path: Path, timestamp: str):
        """Upload backup to S3"""
        try:
            for file_path in backup_path.rglob('*'):
                if file_path.is_file():
                    relative_path = file_path.relative_to(backup_path)
                    s3_key = f"backups/{timestamp}/{relative_path}"
                    
                    self.s3_client.upload_file(
                        str(file_path),
                        self.s3_bucket,
                        str(s3_key)
                    )
        except ClientError as e:
            logger.error(f"S3 upload failed: {str(e)}")
            raise
    
    def _cleanup_old_backups(self):
        """Clean up old backups"""
        max_backups = self.config.get('MAX_BACKUPS', 10)
        backups = sorted(self.backup_dir.glob('backup_*'))
        
        if len(backups) > max_backups:
            for old_backup in backups[:-max_backups]:
                shutil.rmtree(old_backup)
    
    def restore_backup(self, timestamp: str) -> Dict[str, Any]:
        """Restore from a backup"""
        restore_info = {
            'timestamp': timestamp,
            'status': 'success',
            'restored_files': []
        }
        
        try:
            backup_path = self.backup_dir / f"backup_{timestamp}"
            
            # Download from S3 if needed
            if self.config.get('USE_S3_BACKUP'):
                self._download_from_s3(timestamp)
            
            # Restore database
            if (backup_path / 'database.sql').exists():
                self._restore_database(backup_path)
                restore_info['restored_files'].append('database.sql')
            
            # Restore files
            if (backup_path / 'uploads').exists():
                self._restore_files(backup_path)
                restore_info['restored_files'].append('uploads')
            
            if (backup_path / 'reports').exists():
                self._restore_files(backup_path)
                restore_info['restored_files'].append('reports')
            
            return restore_info
            
        except Exception as e:
            logger.error(f"Restore failed: {str(e)}", exc_info=True)
            restore_info['status'] = 'failed'
            restore_info['error'] = str(e)
            return restore_info
    
    def _restore_database(self, backup_path: Path):
        """Restore the database from backup"""
        db_config = self.config['DATABASE']
        dump_file = backup_path / 'database.sql'
        
        # Drop and recreate database
        drop_cmd = [
            'dropdb',
            '-h', db_config['host'],
            '-U', db_config['user'],
            '--if-exists',
            db_config['database']
        ]
        
        create_cmd = [
            'createdb',
            '-h', db_config['host'],
            '-U', db_config['user'],
            db_config['database']
        ]
        
        restore_cmd = [
            'psql',
            '-h', db_config['host'],
            '-U', db_config['user'],
            '-d', db_config['database'],
            '-f', str(dump_file)
        ]
        
        if db_config.get('password'):
            os.environ['PGPASSWORD'] = db_config['password']
        
        try:
            subprocess.run(drop_cmd, check=True)
            subprocess.run(create_cmd, check=True)
            subprocess.run(restore_cmd, check=True)
        finally:
            if db_config.get('password'):
                del os.environ['PGPASSWORD']
    
    def _restore_files(self, backup_path: Path):
        """Restore application files"""
        # Restore uploads
        uploads_backup = backup_path / 'uploads'
        if uploads_backup.exists():
            uploads_dir = Path(self.config['UPLOAD_FOLDER'])
            if uploads_dir.exists():
                shutil.rmtree(uploads_dir)
            shutil.copytree(uploads_backup, uploads_dir)
        
        # Restore reports
        reports_backup = backup_path / 'reports'
        if reports_backup.exists():
            reports_dir = Path(self.config['REPORT_FOLDER'])
            if reports_dir.exists():
                shutil.rmtree(reports_dir)
            shutil.copytree(reports_backup, reports_dir)
    
    def _download_from_s3(self, timestamp: str):
        """Download backup from S3"""
        try:
            backup_path = self.backup_dir / f"backup_{timestamp}"
            backup_path.mkdir(parents=True, exist_ok=True)
            
            paginator = self.s3_client.get_paginator('list_objects_v2')
            for page in paginator.paginate(Bucket=self.s3_bucket, Prefix=f"backups/{timestamp}/"):
                for obj in page.get('Contents', []):
                    key = obj['Key']
                    local_path = backup_path / Path(key).relative_to(f"backups/{timestamp}/")
                    local_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    self.s3_client.download_file(
                        self.s3_bucket,
                        key,
                        str(local_path)
                    )
        except ClientError as e:
            logger.error(f"S3 download failed: {str(e)}")
            raise
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """List available backups"""
        backups = []
        
        # List local backups
        for backup_dir in self.backup_dir.glob('backup_*'):
            backup_info = {
                'timestamp': backup_dir.name.split('_')[1],
                'location': 'local',
                'files': []
            }
            
            # Get backup files
            for item in backup_dir.iterdir():
                if item.is_file() or item.is_dir():
                    backup_info['files'].append(item.name)
            
            backups.append(backup_info)
        
        # List S3 backups if configured
        if self.config.get('USE_S3_BACKUP'):
            try:
                paginator = self.s3_client.get_paginator('list_objects_v2')
                for page in paginator.paginate(Bucket=self.s3_bucket, Prefix='backups/'):
                    for obj in page.get('Contents', []):
                        key = obj['Key']
                        if key.endswith('/'):
                            timestamp = key.split('/')[1]
                            backup_info = {
                                'timestamp': timestamp,
                                'location': 's3',
                                'files': []
                            }
                            
                            # Get backup files from S3
                            for s3_obj in paginator.paginate(
                                Bucket=self.s3_bucket,
                                Prefix=f"backups/{timestamp}/"
                            ).search('Contents'):
                                if not s3_obj['Key'].endswith('/'):
                                    backup_info['files'].append(
                                        Path(s3_obj['Key']).name
                                    )
                            
                            backups.append(backup_info)
            except ClientError as e:
                logger.error(f"Failed to list S3 backups: {str(e)}")
        
        return sorted(backups, key=lambda x: x['timestamp'], reverse=True) 