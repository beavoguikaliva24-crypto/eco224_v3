'use client';

import { Layout, Avatar, Dropdown, MenuProps, Space } from 'antd';
import { UserOutlined, LogoutOutlined, PhoneOutlined, MailOutlined } from '@ant-design/icons';
import { usePathname } from 'next/navigation';
import Link from 'next/link';

const { Header: AntHeader } = Layout;

// Fonction pour obtenir un titre lisible à partir de l'URL
const getTitleFromPath = (path: string) => {
    const segments = path.split('/').filter(Boolean);
    if (segments.length === 1 && segments[0] === 'dashboard') {
        return 'Tableau de Bord Principal';
    }
    if (segments.length > 1) {
        const lastSegment = segments[segments.length - 1];
        return lastSegment.charAt(0).toUpperCase() + lastSegment.slice(1);
    }
    return 'Tableau de Bord';
};


const AppHeader = () => {
    const pathname = usePathname();
    const pageTitle = getTitleFromPath(pathname);

    const items: MenuProps['items'] = [
        {
          key: '1',
          icon: <MailOutlined />,
          label: (
            <span>kaliva.beavogui@example.com</span>
          ),
        },
        {
          key: '2',
          icon: <PhoneOutlined />,
          label: (
            <span>+224 123 456 789</span>
          ),
        },
        {
          type: 'divider',
        },
        {
          key: '4',
          danger: true,
          icon: <LogoutOutlined />,
          label: (
            <Link href="/login">
              Déconnexion
            </Link>
          ),
        },
      ];

  return (
    <AntHeader className="sticky top-0 z-10 flex w-full items-center justify-between bg-white px-6 shadow-sm">
      {/* Côté gauche : Info session / Titre de la page */}
      <h1 className="text-xl font-semibold text-gray-800">{pageTitle}</h1>

      {/* Côté droit : Infos utilisateur */}
      <Dropdown menu={{ items }} placement="bottomRight">
        <a onClick={(e) => e.preventDefault()}>
            <div className="flex cursor-pointer items-center gap-3">
                <div className="text-right">
                    <p className="font-semibold text-gray-700">Kaliva Beavogui</p>
                    <p className="text-xs text-gray-500">Développeur</p>
                </div>
                <Avatar size="large" icon={<UserOutlined />} />
            </div>
        </a>
      </Dropdown>
    </AntHeader>
  );
};

export default AppHeader;