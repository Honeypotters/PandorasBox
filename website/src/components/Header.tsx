// components/Header.tsx
import Image from 'next/image';
import Link from 'next/link';

const Header = () => {
  return (
    <header className="bg-white text-black py-2 px-6 border-b-2 border-black fixed top-0 left-0 right-0 h-16">
        <div className="flex justify-between items-center">
        <div className="flex-shrink-0 left-0 ">
          <Link href="/">
            <Image
              src="/logo.png"
              alt="Logo"
              width={240}
              height={80}
              priority 
            />
          </Link>
        </div>

        <nav className="flex space-x-6">
          <Link href="/dashboard" className="hover:text-gray-600 pl-2 py-2 text-2xl transition-colors duration-200">
            Dashboard
          </Link>
          <Link href="/logs" className="hover:text-gray-600 py-2 text-2xl transition-colors duration-200">
            Logs
          </Link>
          <Link href="/settings" className="hover:text-gray-600 pl-2 py-2 text-2xl transition-colors duration-200">
            Settings
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;
