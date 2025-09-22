import React, { useState } from 'react';
import { Layout, Menu, Avatar, Dropdown, Badge, Button } from 'antd';
import {
  DashboardOutlined,
  ShopOutlined,
  CampaignOutlined,
  MessageOutlined,
  BarChartOutlined,
  SettingOutlined,
  BellOutlined,
  LogoutOutlined,
  UserOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
} from '@ant-design/icons';
import { useNavigate, useLocation } from 'react-router-dom';

const { Header, Sider, Content } = Layout;

interface MerchantLayoutProps {
  children: React.ReactNode;
}

const MerchantLayout: React.FC<MerchantLayoutProps> = ({ children }) => {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    {
      key: '/dashboard',
      icon: <DashboardOutlined />,
      label: '대시보드',
    },
    {
      key: '/stores',
      icon: <ShopOutlined />,
      label: '매장 관리',
    },
    {
      key: '/campaigns',
      icon: <CampaignOutlined />,
      label: '캠페인 관리',
    },
    {
      key: '/reviews',
      icon: <MessageOutlined />,
      label: '리뷰 관리',
    },
    {
      key: '/analytics',
      icon: <BarChartOutlined />,
      label: '분석 리포트',
    },
    {
      key: '/settings',
      icon: <SettingOutlined />,
      label: '설정',
    },
  ];

  const userMenuItems = [
    {
      key: 'profile',
      label: '프로필 설정',
      icon: <UserOutlined />,
    },
    {
      key: 'logout',
      label: '로그아웃',
      icon: <LogoutOutlined />,
    },
  ];

  const handleMenuClick = ({ key }: { key: string }) => {
    navigate(key);
  };

  const handleUserMenuClick = ({ key }: { key: string }) => {
    if (key === 'logout') {
      console.log('로그아웃');
    }
  };

  return (
    <Layout className="merchant-layout">
      <Sider trigger={null} collapsible collapsed={collapsed} width={256}>
        <div style={{ 
          padding: '16px', 
          textAlign: 'center',
          borderBottom: '1px solid #f0f0f0'
        }}>
          {!collapsed ? (
            <h2 style={{ color: '#52c41a', margin: 0 }}>광고주 포털</h2>
          ) : (
            <h2 style={{ color: '#52c41a', margin: 0 }}>MP</h2>
          )}
        </div>
        <Menu
          theme="light"
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={handleMenuClick}
          style={{ height: 'calc(100vh - 64px)', borderRight: 0 }}
        />
      </Sider>
      <Layout>
        <Header style={{ 
          padding: '0 16px', 
          background: '#fff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          boxShadow: '0 2px 8px #f0f1f2'
        }}>
          <Button
            type="text"
            icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
            onClick={() => setCollapsed(!collapsed)}
            style={{ fontSize: '16px', width: 64, height: 64 }}
          />
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <Badge count={3} size="small">
              <BellOutlined style={{ fontSize: '18px' }} />
            </Badge>
            <Dropdown
              menu={{ items: userMenuItems, onClick: handleUserMenuClick }}
              placement="bottomRight"
            >
              <div style={{ 
                display: 'flex', 
                alignItems: 'center', 
                cursor: 'pointer',
                padding: '8px'
              }}>
                <Avatar size="small" icon={<UserOutlined />} />
                <span style={{ marginLeft: '8px' }}>광고주명</span>
              </div>
            </Dropdown>
          </div>
        </Header>
        <Content className="merchant-content">
          {children}
        </Content>
      </Layout>
    </Layout>
  );
};

export default MerchantLayout;
