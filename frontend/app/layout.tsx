import "./globals.css";

export const metadata = {
  title: "MTO Generator",
  description: "Generate Material Take-Off using AI",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}