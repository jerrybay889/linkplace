import React, { useEffect, useState } from 'react';
import { Row, Col, Card, Statistic, Table, Progress, Tag } from 'antd';
import {
  UserOutlined,
  ShopOutlined,
  MessageOutlined,
  DollarCircleOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
} from '@ant-design/icons';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
} from 'recharts';

const Dashboard: React.FC = () => {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 데이터 로딩 시뮬레이션
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  // 통계 데이터
  const stats = [
    {
      title: '전체 사용자',
      value: 12849,
      prefix: <UserOutlined />,
      suffix: '명',
      valueStyle: { color: '#3f8600' },
      trend: 12.8,
      isPositive: true,
    },
    {
      title: '등록 매장',
      value: 3247,
      prefix: <ShopOutlined />,
      suffix: '개',
      valueStyle: { color: '#1890ff' },
      trend: 8.2,
      isPositive: true,
    },
    {
      title: '총 리뷰',
      value: 48392,
      prefix: <MessageOutlined />,
      suffix: '건',
      valueStyle: { color: '#722ed1' },
      trend: 15.6,
      isPositive: true,
    },
    {
      title: '수익',
      value: 2840000,
      prefix: <DollarCircleOutlined />,
      suffix: '원',
      valueStyle: { color: '#f5222d' },
      trend: -2.1,
      isPositive: false,
    },
  ];

  // 월별 가입자 데이터
  const monthlyData = [
    { month: '1월', users: 650, stores: 45 },
    { month: '2월', users: 720, stores: 52 },
    { month: '3월', users: 890, stores: 68 },
    { month: '4월', users: 1200, stores: 85 },
    { month: '5월', users: 980, stores: 72 },
    { month: '6월', users: 1350, stores: 95 },
  ];

  // 리뷰 분포 데이터
  const reviewData = [
    { name: '5점', value: 45, color: '#52c41a' },
    { name: '4점', value: 30, color: '#1890ff' },
    { name: '3점', value: 15, color: '#faad14' },
    { name: '2점', value: 7, color: '#fa8c16' },
    { name: '1점', value: 3, color: '#f5222d' },
  ];

  // 최근 활동 테이블 데이터
  const recentActivities = [
    {
      key: '1',
      user: '김철수',
      action: '리뷰 작성',
      store: '맛있는 카페',
      time: '2분 전',
      status: 'completed',
    },
    {
      key: '2',
      user: '이영희',
      action: '매장 등록',
      store: '새로운 음식점',
      time: '15분 전',
      status: 'pending',
    },
    {
      key: '3',
      user: '박민수',
      action: '캠페인 참여',
      store: '베이커리 하우스',
      time: '1시간 전',
      status: 'completed',
    },
  ];

  const columns = [
    {
      title: '사용자',
      dataIndex: 'user',
      key: 'user',
    },
    {
      title: '활동',
      dataIndex: 'action',
      key: 'action',
    },
    {
      title: '매장',
      dataIndex: 'store',
      key: 'store',
    },
    {
      title: '시간',
      dataIndex: 'time',
      key: 'time',
    },
    {
      title: '상태',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'completed' ? 'green' : 'orange'}>
          {status === 'completed' ? '완료' : '진행중'}
        </Tag>
      ),
    },
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
                color: stat.isPositive ? '#3f8600' : '#f5222d'
              }}>
                {stat.isPositive ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
                {' '}{Math.abs(stat.trend)}% 전월 대비
              </div>
            </Card>
          </Col>
        ))}
      </Row>

      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} lg={16}>
          <Card title="월별 가입 현황" className="chart-container">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={monthlyData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="users" fill="#1890ff" name="사용자" />
                <Bar dataKey="stores" fill="#52c41a" name="매장" />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </Col>
        <Col xs={24} lg={8}>
          <Card title="리뷰 점수 분포" className="chart-container">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={reviewData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  dataKey="value"
                  label={({ name, value }) => `${name}: ${value}%`}
                >
                  {reviewData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={16}>
          <Card title="최근 활동">
            <Table
              columns={columns}
              dataSource={recentActivities}
              pagination={false}
              size="middle"
              loading={loading}
            />
          </Card>
        </Col>
        <Col xs={24} lg={8}>
          <Card title="시스템 상태">
            <div style={{ marginBottom: 16 }}>
              <div style={{ marginBottom: 8 }}>서버 CPU 사용률</div>
              <Progress percent={68} status="active" />
            </div>
            <div style={{ marginBottom: 16 }}>
              <div style={{ marginBottom: 8 }}>메모리 사용률</div>
              <Progress percent={45} />
            </div>
            <div style={{ marginBottom: 16 }}>
              <div style={{ marginBottom: 8 }}>디스크 사용률</div>
              <Progress percent={82} status="exception" />
            </div>
            <div>
              <div style={{ marginBottom: 8 }}>네트워크 상태</div>
              <Progress percent={95} status="success" />
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
