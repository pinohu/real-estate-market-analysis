import React, { Component, ErrorInfo, ReactNode } from 'react';
import { Alert, Container, Header, SpaceBetween } from '@cloudscape-design/components';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
    errorInfo: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
      errorInfo: null,
    };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
    this.setState({
      error,
      errorInfo,
    });
  }

  public render() {
    if (this.state.hasError) {
      return (
        <Container>
          <SpaceBetween size="l">
            <Header
              variant="h1"
              description="We're sorry, something went wrong"
            >
              Error
            </Header>
            <Alert
              type="error"
              header="An error occurred"
            >
              {this.state.error && this.state.error.toString()}
              <br />
              {this.state.errorInfo && this.state.errorInfo.componentStack}
            </Alert>
          </SpaceBetween>
        </Container>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary; 