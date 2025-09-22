import React from 'react';
import { Card, Table, Tag } from 'antd';

const Stores: React.FC = () => {
  const columns = [
    { title: '매장명', dataIndex: 'name', key: 'name' },
    { title: '주소', dataIndex: 'address', key: 'address' },
    { title: '카테고리', dataIndex: 'category', key: 'category', render: (cat: string) => <Tag>{cat}</Tag> },
    { title: '평점', dataIndex: 'rating', key: 'rating', render: (rating: number) => `⭐ ${rating}` },
  ];

  const data = [
    { key: 1, name: '맛있는 카페', address: '서울 강남구', category: '카페', rating: 4.5 },
    { key: 2, name: '피자하우스', address: '서울 마포구', category: '음식점', rating: 4.2 },
  ];

  return (
    <Card title="매장 관리">
      <Table columns={columns} dataSource={data} />
    </Card>
  );
};

export default Stores;
