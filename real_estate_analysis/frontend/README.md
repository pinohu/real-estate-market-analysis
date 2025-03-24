# Real Estate Analysis Platform - Frontend

This is the frontend application for the Real Estate Analysis Platform. It's built with React, TypeScript, and Material-UI.

## Environment Setup

The application uses different environment files for various deployment scenarios:

### Environment Files

1. `.env` - Default environment variables
2. `.env.development` - Development environment variables
3. `.env.production` - Production environment variables
4. `.env.test` - Testing environment variables
5. `.env.local` - Local environment variables (git ignored)
6. `.env.development.local` - Local development environment variables (git ignored)
7. `.env.test.local` - Local test environment variables (git ignored)
8. `.env.production.local` - Local production environment variables (git ignored)

### Required Environment Variables

#### API Configuration
- `REACT_APP_API_BASE_URL` - Base URL for the API endpoints

#### Feature Flags
- `REACT_APP_ENABLE_ANALYTICS` - Enable/disable analytics tracking
- `REACT_APP_ENABLE_NOTIFICATIONS` - Enable/disable notifications

#### Application Settings
- `REACT_APP_MAX_FILE_SIZE` - Maximum file size for uploads (in bytes)
- `REACT_APP_SUPPORTED_FILE_TYPES` - Comma-separated list of supported file types

#### External Services
- `REACT_APP_GOOGLE_MAPS_API_KEY` - API key for Google Maps integration
- `REACT_APP_SENTRY_DSN` - Sentry DSN for error tracking

#### Environment-Specific Settings
- `REACT_APP_ENABLE_DEV_TOOLS` - Enable/disable development tools
- `REACT_APP_LOG_LEVEL` - Logging level (debug, info, warn, error)
- `REACT_APP_ENABLE_HOT_RELOAD` - Enable/disable hot reloading
- `REACT_APP_ENABLE_SOURCE_MAPS` - Enable/disable source maps

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```
3. Copy the appropriate environment file:
   ```bash
   cp .env.example .env.local
   ```
4. Update the environment variables in `.env.local` with your values
5. Start the development server:
   ```bash
   npm start
   ```

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App

## Development Guidelines

1. Follow the TypeScript and ESLint configurations
2. Use Prettier for code formatting
3. Write unit tests for new components and features
4. Update documentation when making changes

## Deployment

The application can be deployed to various environments:

### Development
```bash
npm run build:dev
```

### Production
```bash
npm run build:prod
```

### Testing
```bash
npm run build:test
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@realestateanalysis.com or join our Slack channel. 