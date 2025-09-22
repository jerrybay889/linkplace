import React from 'react';
import { Card, Table, Tag, Progress } from 'antd';

const Campaigns: React.FC = () => {
  const columns = [
    { title: '캠페인명', dataIndex: 'name', key: 'name' },
    { title: '광고주', dataIndex: 'merchant', key: 'merchant' },
    { title: '상태', dataIndex: 'status', key: 'status', render: (status: string) => 
      <Tag color={status === 'active' ? 'green' : status === 'pending' ? 'orange' : 'red'}>{status}</Tag>
    },
    { title: '진행률', dataIndex: 'progress', key: 'progress', render: (progress: number) => 
      <Progress percent={progress} size="small" />
    },
  ];

  const data = [
    { key: 1, name: '신규 오픈 이벤트', merchant: 'ABC 카페', status: 'active', progress: 75 },
    { key: 2, name: '할인 쿠폰 캠페인', merchant: 'XYZ 레스토랑', status: 'pending', progress: 30 },
  ];

  return (
    <Card title="캠페인 관리">
      <Table columns={columns} dataSource={data} />
    </Card>
  );
};

export default Campaigns;
