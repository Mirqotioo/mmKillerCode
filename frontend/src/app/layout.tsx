import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Movie Montage Creator",
  description: "Create video montages from movies based on written summaries",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="it">
      <body className={inter.className}>
        <main className="min-h-screen bg-gray-50">
          <header className="bg-blue-600 text-white p-4 shadow-md">
            <div className="container mx-auto">
              <h1 className="text-2xl font-bold">Movie Montage Creator</h1>
              <p className="text-sm opacity-80">Crea montaggi video basati su riassunti scritti</p>
            </div>
          </header>
          <div className="container mx-auto p-4">
            {children}
          </div>
          <footer className="bg-gray-100 p-4 border-t">
            <div className="container mx-auto text-center text-gray-600 text-sm">
              &copy; {new Date().getFullYear()} Movie Montage Creator
            </div>
          </footer>
        </main>
      </body>
    </html>
  );
}
