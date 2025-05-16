// server.js
const express = require('express');
const multer = require('multer');
const fetch = require('node-fetch');
const fs = require('fs');
const path = require('path');
const upload = multer({ dest: 'uploads/' });

const app = express();
const PORT = process.env.PORT || 3000;
const DISCORD_WEBHOOK = 'https://discord.com/api/webhooks/1372915239640629248/N1ogZd_OKJ-jIlPoeE4F2Jt6p3-thxJ9x7kqrRL7V5GJLeaq9pSgko8qdTI9YgufPXiY';

app.post('/upload', upload.single('image'), async (req, res) => {
  const file = req.file;
  if (!file) return res.status(400).send('No file uploaded');

  const filePath = path.join(__dirname, file.path);

  const formData = new FormData();
  formData.append('file', fs.createReadStream(filePath));

  try {
    await fetch(DISCORD_WEBHOOK, {
      method: 'POST',
      body: formData
    });
    fs.unlinkSync(filePath);
    res.send('OK');
  } catch (err) {
    fs.unlinkSync(filePath);
    res.status(500).send('Upload failed');
  }
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
