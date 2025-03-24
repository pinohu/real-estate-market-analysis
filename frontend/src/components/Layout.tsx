import React from 'react';
import {
  AppLayout,
  ContentLayout,
  Header,
  SideNavigation,
  Spinner,
} from '@cloudscape-design/components';

interface LayoutProps {
  children: React.ReactNode;
  activeHref?: string;
  isLoading?: boolean;
}

const Layout: React.FC<LayoutProps> = ({ children, activeHref, isLoading }) => {
  const navigationItems = [
    {
      type: 'section',
      text: 'Main',
      items: [
        { type: 'link', text: 'Dashboard', href: '/' },
        { type: 'link', text: 'Property Analysis', href: '/property-analysis' },
        { type: 'link', text: 'Market Analysis', href: '/market-analysis' },
      ]
    },
    {
      type: 'section',
      text: 'Configuration',
      items: [
        { type: 'link', text: 'Settings', href: '/settings' }
      ]
    }
  ] as const;

  return (
    <AppLayout
      navigation={
        <SideNavigation
          activeHref={activeHref}
          items={navigationItems}
          header={{ text: 'Real Estate Strategist', href: '/' }}
        />
      }
      content={
        <ContentLayout
          header={
            <Header
              variant="h1"
              description="Make informed real estate investment decisions"
            >
              Real Estate Market Analysis
              {isLoading && <Spinner />}
            </Header>
          }
        >
          {children}
        </ContentLayout>
      }
      toolsHide={true}
    />
  );
};

export default Layout; 