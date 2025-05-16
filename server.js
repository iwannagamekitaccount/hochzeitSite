const express = require('express');
const multer = require('multer');
const fs = require('fs');
const FormData = require('form-data');
const fetch = require('node-fetch');
const path = require('path');

const app = express();
const upload = multer({ dest: 'uploads/' });
const PORT = process.env.PORT || 10000;
const DISCORD_WEBHOOK = process.env.DISCORD_WEBHOOK;

app.post('/upload', upload.single('image'), async (req, res) => {
  const file = req.file;
  if (!file) return res.status(400).send('Kein Bild hochgeladen.');

  const form = new FormData();
  form.append('file', fs.createReadStream(file.path));

  try {
    await fetch(DISCORD_WEBHOOK, {
      method: 'POST',
      body: form,
    });
    fs.unlinkSync(file.path); // Bild löschen
    res.send('Bild erfolgreich an Discord gesendet!');
  } catch (err) {
    fs.unlinkSync(file.path);
    res.status(500).send('Fehler beim Senden an Discord');
  }
});

app.listen(PORT, () => console.log(`Server läuft auf Port ${PORT}`));
