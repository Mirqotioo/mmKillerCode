export const metadata = {
  title: 'mmKiller - Movie Montage Creator',
  description: 'Crea montaggi video basati su riassunti scritti',
}

export default function RootLayout({ children })  {
  return (
    <html lang="it">
      <body>{children}</body>
    </html>
  )
}
