'use client';

import { useState } from 'react';
import { Layout, Menu } from 'antd';
import {
  UserOutlined,
  TeamOutlined,
  ReadOutlined,
  BarChartOutlined,
  SettingOutlined,
  LogoutOutlined,
} from '@ant-design/icons';
import Link from 'next/link';

const { Sider } = Layout;

const Sidebar = () => {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <Sider collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)} theme="light">
      <div className="demo-logo-vertical p-4 text-center text-lg font-bold text-gray-700">
        {collapsed ? 'E' : 'ECOLE-224'}
      </div>
      <Menu theme="light" defaultSelectedKeys={['1']} mode="inline">
        <Menu.Item key="1" icon={<BarChartOutlined />}>
          <Link href="/dashboard">Tableau de bord</Link>
        </Menu.Item>
        <Menu.Item key="2" icon={<UserOutlined />}>
          <Link href="/dashboard/students">Élèves</Link>
        </Menu.Item>
        <Menu.Item key="3" icon={<TeamOutlined />}>
          <Link href="/dashboard/teachers">Enseignants</Link>
        </Menu.Item>
        <Menu.Item key="4" icon={<ReadOutlined />}>
          <Link href="/dashboard/courses">Matières</Link>
        </Menu.Item>
        <Menu.Item key="5" icon={<SettingOutlined />}>
          <Link href="/dashboard/settings">Paramètres</Link>
        </Menu.Item>
        <Menu.Item key="sub1" icon={<LogoutOutlined />} className="absolute bottom-0 w-full">
          <Link href="/login">Déconnexion</Link>
        </Menu.Item>
      </Menu>
    </Sider>
  );
};

export default Sidebar;