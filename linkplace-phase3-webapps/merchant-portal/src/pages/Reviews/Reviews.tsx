import React from 'react';
import { Card, List, Rate, Avatar, Tag, Button } from 'antd';
import { UserOutlined, MessageOutlined } from '@ant-design/icons';

const Reviews: React.FC = () => {
  const reviews = [
    {
      id: 1,
      user: '김철수',
      store: '강남 본점',
      rating: 5,
      content: '커피가 정말 맛있어요!',
      date: '2024-01-15',
      replied: false
    },
    {
      id: 2,
      user: '이영희',
      store: '홍대 지점',
      rating: 4,
      content: '분위기도 좋고 직원분들도 친절해요.',
      date: '2024-01-14',
      replied: true
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
              <Tag color={item.replied ? 'green' : 'orange'}>
                {item.replied ? '답변완료' : '미답변'}
              </Tag>,
              !item.replied && <Button type="link" icon={<MessageOutlined />}>답변하기</Button>
            ]}
          >
            <List.Item.Meta
              avatar={<Avatar icon={<UserOutlined />} />}
              title={`${item.user} - ${item.store}`}
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
