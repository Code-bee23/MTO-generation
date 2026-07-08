import UploadBox from "@/components/UploadBox";

export default function Home() {
  return (
    <main className="container">
      <h1>MTO Generator</h1>

      <p>
        Upload an Isometric Drawing (PDF, PNG, JPG or JPEG) to generate
        Material Take-Off.
      </p>

      <UploadBox />
    </main>
  );
}