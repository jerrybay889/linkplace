import React, { useEffect, useState } from 'react';
import { Row, Col, Card, Statistic, Table, Tag } from 'antd';
import {
  ShopOutlined,
  CampaignOutlined,
  MessageOutlined,
  DollarCircleOutlined,
  ArrowUpOutlined,
} from '@ant-design/icons';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
} from 'recharts';

const Dashboard: React.FC = () => {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => setLoading(false), 1000);
  }, []);

  // 통계 데이터
  const stats = [
    {
      title: '등록 매장',
      value: 12,
      prefix: <ShopOutlined />,
      suffix: '개',
      valueStyle: { color: '#1890ff' },
    },
    {
      title: '진행 캠페인',
      value: 5,
      prefix: <CampaignOutlined />,
      suffix: '건',
      valueStyle: { color: '#52c41a' },
    },
    {
      title: '총 리뷰',
      value: 1247,
      prefix: <MessageOutlined />,
      suffix: '개',
      valueStyle: { color: '#722ed1' },
    },
    {
      title: '이번 달 수익',
      value: 450000,
      prefix: <DollarCircleOutlined />,
      suffix: '원',
      valueStyle: { color: '#f5222d' },
    },
  ];

  // 월별 수익 데이터
  const revenueData = [
    { month: '1월', revenue: 320000 },
    { month: '2월', revenue: 380000 },
    { month: '3월', revenue: 420000 },
    { month: '4월', revenue: 450000 },
    { month: '5월', revenue: 410000 },
    { month: '6월', revenue: 480000 },
  ];

  // 최근 캠페인 데이터
  const recentCampaigns = [
    {
      key: '1',
      name: '신규 오픈 이벤트',
      status: 'active',
      progress: 75,
      budget: '50만원',
    },
    {
      key: '2',
      name: '할인 쿠폰 캠페인',
      status: 'pending',
      progress: 30,
      budget: '30만원',
    },
  ];

  const columns = [
    { title: '캠페인명', dataIndex: 'name', key: 'name' },
    { 
      title: '상태', 
      dataIndex: 'status', 
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'active' ? 'green' : 'orange'}>
          {status === 'active' ? '진행중' : '대기중'}
        </Tag>
      )
    },
    { title: '예산', dataIndex: 'budget', key: 'budget' },
  ];

  return (
    <div>
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        {stats.map((stat, index) => (
          <Col xs={24} sm={12} md={6} key={index}>
            <Card className="stats-card" loading={loading}>
              <Statistic
                title={stat.title}
                value={stat.value}
                prefix={stat.prefix}
                suffix={stat.suffix}
                valueStyle={stat.valueStyle}
              />
              <div style={{ 
                marginTop: 8, 
                fontSize: '12px',
                color: '#3f8600'
              }}>
                <ArrowUpOutlined /> 12% 전월 대비
              </div>
            </Card>
          </Col>
        ))}
      </Row>

      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} lg={16}>
          <Card title="월별 수익 현황" className="chart-container">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={revenueData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip formatter={(value) => [`${value.toLocaleString()}원`, '수익']} />
                <Line type="monotone" dataKey="revenue" stroke="#52c41a" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </Card>
        </Col>
        <Col xs={24} lg={8}>
          <Card title="최근 캠페인">
            <Table
              columns={columns}
              dataSource={recentCampaigns}
              pagination={false}
              size="small"
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
