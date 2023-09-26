import NextAuth from "next-auth"
import CredentialsProvider from "next-auth/providers/credentials";
import axios from "axios";
import dns from 'node:dns';
dns.setDefaultResultOrder('ipv4first');
const apiURL = process.env.NEXT_PUBLIC_API_URL;

const urlMaker = (path: string) => `${apiURL}${path}`;

const handler = NextAuth({
  session: {
    strategy: "jwt",
  },
  providers: [
    CredentialsProvider({
      name: "Sign in",
      credentials: {
        username: { label: "Username", type: "text" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials, req) {
        const url = urlMaker("/api/login/");
        console.log(url);
        try{
            const res = await fetch(url, {
            method: 'POST',
            body: JSON.stringify(credentials),
            headers: { "Content-Type": "application/json" }
            })
            const user = await res.json()
            if ( res.ok && user) {
                console.log(user)
                return user
            }
        } catch (err) {
          console.log(err);
        }
        

        return { id: 1, name: 'J Smith', email: 'jsmith@example.com' }
    },
    }),
  ],
})

export { handler as GET, handler as POST }