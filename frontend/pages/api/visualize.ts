// pages/api/visualize.ts or wherever you're making the request
import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    try {
      const response = await axios.post(`${API_URL}/visualize`, req.body);
      res.status(200).json(response.data);
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        // Forward the status code and error message from the Flask server
        res.status(error.response.status).json(error.response.data);
      } else {
        res.status(500).json({ error: 'An unexpected error occurred' });
      }
    }
  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}