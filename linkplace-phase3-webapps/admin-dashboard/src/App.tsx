import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import koKR from 'antd/locale/ko_KR';
import dayjs from 'dayjs';
import 'dayjs/locale/ko';

import AdminLayout from '@/components/Layout/AdminLayout';
import Dashboard from '@/pages/Dashboard/Dashboard';
import Users from '@/pages/Users/Users';
import Stores from '@/pages/Stores/Stores';
import Reviews from '@/pages/Reviews/Reviews';
import Campaigns from '@/pages/Campaigns/Campaigns';
import Merchants from '@/pages/Merchants/Merchants';
import Settings from '@/pages/Settings/Settings';

// dayjs 한국어 설정
dayjs.locale('ko');

const App: React.FC = () => {
  return (
    <ConfigProvider 
      locale={koKR}
      theme={{
        token: {
          colorPrimary: '#1890ff',
          borderRadius: 6,
        },
      }}
    >
      <Router>
        <AdminLayout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/users" element={<Users />} />
            <Route path="/stores" element={<Stores />} />
            <Route path="/reviews" element={<Reviews />} />
            <Route path="/campaigns" element={<Campaigns />} />
            <Route path="/merchants" element={<Merchants />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </AdminLayout>
      </Router>
    </ConfigProvider>
  );
};

export default App;
