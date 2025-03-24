import React, { PropsWithChildren } from 'react';
import { AppLayout, TopNavigation, SideNavigation } from '@cloudscape-design/components';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';

const Layout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const navigationItems = [
    { type: 'link' as const, text: 'Dashboard', href: '/' },
    { type: 'link' as const, text: 'Market Analysis', href: '/market-analysis' },
    { type: 'link' as const, text: 'Property Comparison', href: '/property-comparison' },
  ];

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
        content={<Outlet />}
        navigation={
          <SideNavigation
            activeHref={location.pathname}
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