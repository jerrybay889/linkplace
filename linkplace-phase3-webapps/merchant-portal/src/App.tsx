import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import koKR from 'antd/locale/ko_KR';
import dayjs from 'dayjs';
import 'dayjs/locale/ko';

import MerchantLayout from '@/components/Layout/MerchantLayout';
import Dashboard from '@/pages/Dashboard/Dashboard';
import Stores from '@/pages/Stores/Stores';
import Campaigns from '@/pages/Campaigns/Campaigns';
import Reviews from '@/pages/Reviews/Reviews';
import Analytics from '@/pages/Analytics/Analytics';
import Settings from '@/pages/Settings/Settings';

// dayjs 한국어 설정
dayjs.locale('ko');

const App: React.FC = () => {
  return (
    <ConfigProvider 
      locale={koKR}
      theme={{
        token: {
          colorPrimary: '#52c41a',
          borderRadius: 6,
        },
      }}
    >
      <Router>
        <MerchantLayout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/stores" element={<Stores />} />
            <Route path="/campaigns" element={<Campaigns />} />
            <Route path="/reviews" element={<Reviews />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </MerchantLayout>
      </Router>
    </ConfigProvider>
  );
};

export default App;
