import Head from "next/head";
import App from './components/App';

export default function Home() {
  return (
    <>
    <Head>
      <title>My Awesome app</title>
      <link
        rel="stylesheet" href="https://cdn.jsdelivr.net/npm/siimple@3.1.1/dist/siimple.min.css"
      />
    </Head>
    <App /> 
  </>
  )
}