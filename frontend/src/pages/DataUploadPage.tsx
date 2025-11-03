import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  Alert,
  CircularProgress,
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import api from '../utils/api';

const DataUploadPage: React.FC = () => {
  const [files, setFiles] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFiles(Array.from(event.target.files));
      setError(null);
      setResult(null);
    }
  };

  const handleUpload = async () => {
    if (files.length === 0) {
      setError('Пожалуйста, выберите файлы для загрузки');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const formData = new FormData();
      files.forEach((file) => {
        formData.append('files', file);
      });

      const response = await api.post('/api/files/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка при загрузке файлов');
    } finally {
      setUploading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Загрузка данных
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Загрузите Excel файлы с данными о недвижимости (.xlsx, .xls)
      </Typography>

      <Paper sx={{ p: 3, mt: 2 }}>
        <Box sx={{ mb: 2 }}>
          <input
            accept=".xlsx,.xls"
            style={{ display: 'none' }}
            id="file-upload"
            multiple
            type="file"
            onChange={handleFileChange}
          />
          <label htmlFor="file-upload">
            <Button
              variant="contained"
              component="span"
              startIcon={<CloudUploadIcon />}
            >
              Выбрать файлы
            </Button>
          </label>
        </Box>

        {files.length > 0 && (
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2">Выбранные файлы:</Typography>
            <ul>
              {files.map((file, index) => (
                <li key={index}>{file.name}</li>
              ))}
            </ul>
          </Box>
        )}

        <Button
          variant="contained"
          color="primary"
          onClick={handleUpload}
          disabled={files.length === 0 || uploading}
          sx={{ mb: 2 }}
        >
          {uploading ? <CircularProgress size={24} /> : 'Загрузить'}
        </Button>

        {error && <Alert severity="error">{error}</Alert>}

        {result && (
          <Box sx={{ mt: 2 }}>
            <Alert severity="success">
              Успешно обработано файлов: {result.files_processed}
            </Alert>
            <Box sx={{ mt: 2 }}>
              <Typography variant="h6">Извлеченные данные:</Typography>
              <pre style={{ overflow: 'auto', maxHeight: '400px' }}>
                {JSON.stringify(result.data, null, 2)}
              </pre>
            </Box>
          </Box>
        )}
      </Paper>
    </Box>
  );
};

export default DataUploadPage;
