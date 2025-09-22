import React from 'react';
import { Card, List, Rate, Avatar, Tag } from 'antd';
import { UserOutlined } from '@ant-design/icons';

const Reviews: React.FC = () => {
  const reviews = [
    {
      id: 1,
      user: '김철수',
      store: '맛있는 카페',
      rating: 5,
      content: '정말 맛있었어요! 추천합니다.',
      date: '2024-01-15',
      status: 'approved'
    },
    {
      id: 2,
      user: '이영희',
      store: '피자하우스',
      rating: 4,
      content: '가격대비 괜찮은 것 같습니다.',
      date: '2024-01-14',
      status: 'pending'
    },
  ];

  return (
    <Card title="리뷰 관리">
      <List
        itemLayout="vertical"
        dataSource={reviews}
        renderItem={item => (
          <List.Item
            actions={[
              <Tag color={item.status === 'approved' ? 'green' : 'orange'}>
                {item.status === 'approved' ? '승인됨' : '검토중'}
              </Tag>
            ]}
          >
            <List.Item.Meta
              avatar={<Avatar icon={<UserOutlined />} />}
              title={<div>{item.user} - {item.store}</div>}
              description={
                <div>
                  <Rate disabled defaultValue={item.rating} />
                  <div style={{ marginTop: 8 }}>{item.content}</div>
                  <div style={{ marginTop: 4, color: '#666', fontSize: '12px' }}>{item.date}</div>
                </div>
              }
            />
          </List.Item>
        )}
      />
    </Card>
  );
};

export default Reviews;
