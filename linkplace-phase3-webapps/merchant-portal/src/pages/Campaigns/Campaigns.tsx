import React from 'react';
import { Card, Table, Tag, Progress, Button, Space } from 'antd';
import { PlusOutlined, EditOutlined, PauseCircleOutlined } from '@ant-design/icons';

const Campaigns: React.FC = () => {
  const columns = [
    { title: '캠페인명', dataIndex: 'name', key: 'name' },
    { title: '예산', dataIndex: 'budget', key: 'budget' },
    { title: '기간', dataIndex: 'period', key: 'period' },
    { title: '진행률', dataIndex: 'progress', key: 'progress', 
      render: (progress: number) => <Progress percent={progress} size="small" />
    },
    { title: '상태', dataIndex: 'status', key: 'status',
      render: (status: string) => <Tag color={status === 'active' ? 'green' : 'orange'}>{status}</Tag>
    },
    {
      title: '작업',
      key: 'actions',
      render: () => (
        <Space>
          <Button type="text" icon={<EditOutlined />} />
          <Button type="text" icon={<PauseCircleOutlined />} />
        </Space>
      ),
    },
  ];

  const data = [
    { key: 1, name: '신규 오픈 이벤트', budget: '50만원', period: '2024.01.01 ~ 2024.01.31', progress: 75, status: 'active' },
  ];

  return (
    <Card title="캠페인 관리" extra={<Button type="primary" icon={<PlusOutlined />}>캠페인 생성</Button>}>
      <Table columns={columns} dataSource={data} />
    </Card>
  );
};

export default Campaigns;
