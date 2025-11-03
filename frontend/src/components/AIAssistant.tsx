import React, { useState } from 'react';
import {
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Divider,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import api from '../utils/api';

interface AIMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  updatedParameters?: any;
}

interface AIAssistantProps {
  propertyData: any;
  result?: any;
  onDataUpdate?: (updatedData: any) => void;
}

const AIAssistant: React.FC<AIAssistantProps> = ({
  propertyData,
  result,
  onDataUpdate,
}) => {
  const [message, setMessage] = useState('');
  const [conversation, setConversation] = useState<AIMessage[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!message.trim()) return;

    const userMessage: AIMessage = {
      role: 'user',
      content: message,
      timestamp: new Date(),
    };

    setConversation((prev) => [...prev, userMessage]);
    setMessage('');
    setLoading(true);

    try {
      const context = {
        property_data: propertyData,
        calculation_result: result,
      };

      const response = await api.post('/api/ai/conversation', {
        message: userMessage.content,
        context,
      });

      const assistantMessage: AIMessage = {
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date(),
        updatedParameters: response.data.updated_parameters,
      };

      setConversation((prev) => [...prev, assistantMessage]);

      // Если AI вернул обновленные параметры, передаем их родителю
      if (response.data.updated_parameters && onDataUpdate) {
        onDataUpdate(response.data.updated_parameters);
      }
    } catch (error: any) {
      const errorMessage: AIMessage = {
        role: 'assistant',
        content: `Ошибка: ${error.response?.data?.detail || error.message}`,
        timestamp: new Date(),
      };
      setConversation((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper sx={{ p: 2, mt: 2 }}>
      <Typography variant="h6" gutterBottom>
        AI Ассистент
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Задайте вопросы об оценке или попросите AI помочь с параметрами
      </Typography>

      <Box
        sx={{
          height: '400px',
          overflow: 'auto',
          border: '1px solid #e0e0e0',
          borderRadius: 1,
          p: 2,
          mb: 2,
          bgcolor: '#f5f5f5',
        }}
      >
        {conversation.length === 0 ? (
          <Typography variant="body2" color="text.secondary">
            Начните разговор с AI ассистентом...
          </Typography>
        ) : (
          <List>
            {conversation.map((msg, index) => (
              <React.Fragment key={index}>
                <ListItem
                  sx={{
                    justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
                  }}
                >
                  <Box
                    sx={{
                      maxWidth: '70%',
                      bgcolor: msg.role === 'user' ? 'primary.light' : 'grey.200',
                      p: 1.5,
                      borderRadius: 2,
                    }}
                  >
                    <Typography variant="body2">{msg.content}</Typography>
                    {msg.updatedParameters && (
                      <Typography variant="caption" color="success.main" sx={{ mt: 1 }}>
                        AI предложил обновить параметры
                      </Typography>
                    )}
                  </Box>
                </ListItem>
                {index < conversation.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        )}
      </Box>

      <Box sx={{ display: 'flex', gap: 1 }}>
        <TextField
          fullWidth
          multiline
          maxRows={4}
          placeholder="Задайте вопрос AI ассистенту..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
          disabled={loading}
        />
        <Button
          variant="contained"
          endIcon={loading ? <CircularProgress size={20} /> : <SendIcon />}
          onClick={handleSend}
          disabled={loading || !message.trim()}
        >
          Отправить
        </Button>
      </Box>
    </Paper>
  );
};

export default AIAssistant;
