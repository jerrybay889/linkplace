import React from 'react';
import { Card, Row, Col, Statistic } from 'antd';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const Analytics: React.FC = () => {
  const data = [
    { name: '1월', visits: 1200, reviews: 45 },
    { name: '2월', visits: 1380, reviews: 52 },
    { name: '3월', visits: 1550, visits: 68 },
  ];

  return (
    <div>
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col span={8}>
          <Card>
            <Statistic title="총 방문자" value={15420} suffix="명" />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic title="전환율" value={12.5} suffix="%" />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic title="평균 평점" value={4.3} suffix="/5.0" />
          </Card>
        </Col>
      </Row>

      <Card title="월별 분석">
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="visits" fill="#1890ff" />
            <Bar dataKey="reviews" fill="#52c41a" />
          </BarChart>
        </ResponsiveContainer>
      </Card>
    </div>
  );
};

export default Analytics;
