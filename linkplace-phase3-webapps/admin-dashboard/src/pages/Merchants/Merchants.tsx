import React from 'react';
import { Card, Table, Tag, Avatar } from 'antd';
import { ShopOutlined } from '@ant-design/icons';

const Merchants: React.FC = () => {
  const columns = [
    { 
      title: '광고주', 
      dataIndex: 'name', 
      key: 'name',
      render: (name: string) => (
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <Avatar icon={<ShopOutlined />} style={{ marginRight: 8 }} />
          {name}
        </div>
      )
    },
    { title: '업종', dataIndex: 'category', key: 'category' },
    { title: '매장수', dataIndex: 'storeCount', key: 'storeCount', render: (count: number) => `${count}개` },
    { title: '상태', dataIndex: 'status', key: 'status', render: (status: string) => 
      <Tag color={status === 'active' ? 'green' : 'red'}>{status === 'active' ? '활성' : '비활성'}</Tag>
    },
  ];

  const data = [
    { key: 1, name: 'ABC 카페 체인', category: '카페', storeCount: 15, status: 'active' },
    { key: 2, name: 'XYZ 레스토랑', category: '음식점', storeCount: 8, status: 'active' },
  ];

  return (
    <Card title="광고주 관리">
      <Table columns={columns} dataSource={data} />
    </Card>
  );
};

export default Merchants;
