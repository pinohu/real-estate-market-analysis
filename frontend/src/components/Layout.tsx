import React, { PropsWithChildren } from 'react';
import { AppLayout, TopNavigation, SideNavigation, Spinner } from '@cloudscape-design/components';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';

interface LayoutProps {
  children?: React.ReactNode;
  activeHref?: string;
  isLoading?: boolean;
}

const Layout: React.FC<LayoutProps> = ({ children, activeHref, isLoading }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const navigationItems = [
    { type: 'link' as const, text: 'Dashboard', href: '/' },
    { type: 'link' as const, text: 'Market Analysis', href: '/market-analysis' },
    { type: 'link' as const, text: 'Property Comparison', href: '/property-comparison' },
  ];

  const content = isLoading ? (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
      <Spinner size="large" />
    </div>
  ) : (
    children || <Outlet />
  );

  return (
    <div>
      <TopNavigation
        identity={{
          href: '/',
          title: 'Real Estate Strategist',
        }}
        utilities={[
          {
            type: 'button',
            text: 'Settings',
            onClick: () => navigate('/settings'),
          },
        ]}
      />
      <AppLayout
        content={content}
        navigation={
          <SideNavigation
            activeHref={activeHref || location.pathname}
            items={navigationItems}
            header={{
              href: '/',
              text: 'Navigation'
            }}
            onFollow={e => {
              e.preventDefault();
              navigate(e.detail.href);
            }}
          />
        }
        toolsHide={true}
        navigationWidth={250}
      />
    </div>
  );
};

export default Layout; 