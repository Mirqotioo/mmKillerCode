import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { useRouter, useSearchParams } from 'next/navigation';
import UploadPage from '@/app/upload/page';
import ReviewPage from '@/app/review/page';
import PreviewPage from '@/app/preview/page';
import apiClient from '@/lib/api/apiClient';

// Mock dei moduli Next.js
jest.mock('next/navigation', () => ({
  useRouter: jest.fn(),
  useSearchParams: jest.fn(),
}));

// Mock del client API
jest.mock('@/lib/api/apiClient', () => ({
  uploadVideo: jest.fn(),
  processVideo: jest.fn(),
  updateMatches: jest.fn(),
  generateMontage: jest.fn(),
  getDownloadUrl: jest.fn(),
}));

describe('UploadPage', () => {
  const mockRouter = { push: jest.fn() };
  
  beforeEach(() => {
    useRouter.mockReturnValue(mockRouter);
    apiClient.uploadVideo.mockResolvedValue({ job_id: 'test_job' });
    apiClient.processVideo.mockResolvedValue({});
  });
  
  test('renders upload form correctly', () => {
    render(<UploadPage />);
    
    expect(screen.getByText('Carica Video e Riassunto')).toBeInTheDocument();
    expect(screen.getByText('Carica e Procedi')).toBeInTheDocument();
    expect(screen.getByLabelText('Video File')).toBeInTheDocument();
    expect(screen.getByLabelText('Riassunto Scritto')).toBeInTheDocument();
  });
  
  test('handles form submission', async () => {
    render(<UploadPage />);
    
    // Simula l'inserimento del riassunto
    fireEvent.change(screen.getByLabelText('Riassunto Scritto'), {
      target: { value: 'Questo è un riassunto di test.' },
    });
    
    // Simula il caricamento del file
    const file = new File(['test content'], 'test.mp4', { type: 'video/mp4' });
    const fileInput = screen.getByLabelText('Video File');
    Object.defineProperty(fileInput, 'files', {
      value: [file],
    });
    fireEvent.change(fileInput);
    
    // Simula l'invio del form
    fireEvent.click(screen.getByText('Carica e Procedi'));
    
    // Verifica che le API siano state chiamate
    await waitFor(() => {
      expect(apiClient.uploadVideo).toHaveBeenCalledWith(file, 'Questo è un riassunto di test.');
      expect(apiClient.processVideo).toHaveBeenCalledWith('test_job');
      expect(mockRouter.push).toHaveBeenCalledWith('/review?jobId=test_job');
    });
  });
});

describe('ReviewPage', () => {
  const mockRouter = { push: jest.fn() };
  
  beforeEach(() => {
    useRouter.mockReturnValue(mockRouter);
    useSearchParams.mockReturnValue(new URLSearchParams('jobId=test_job'));
    apiClient.updateMatches.mockResolvedValue({});
    apiClient.generateMontage.mockResolvedValue({});
  });
  
  test('renders review page correctly', async () => {
    render(<ReviewPage />);
    
    // Verifica che la pagina di caricamento sia mostrata inizialmente
    expect(screen.getByText('Caricamento in corso...')).toBeInTheDocument();
    
    // Attendi che i dati simulati siano caricati
    await waitFor(() => {
      expect(screen.getByText('Rivedi e Modifica le Corrispondenze')).toBeInTheDocument();
      expect(screen.getByText('Frasi del Riassunto')).toBeInTheDocument();
      expect(screen.getByText('Scene Disponibili')).toBeInTheDocument();
      expect(screen.getByText('Finalizza Montaggio')).toBeInTheDocument();
    });
  });
  
  test('handles finalization', async () => {
    render(<ReviewPage />);
    
    // Attendi che i dati simulati siano caricati
    await waitFor(() => {
      expect(screen.getByText('Finalizza Montaggio')).toBeInTheDocument();
    });
    
    // Simula il clic sul pulsante di finalizzazione
    fireEvent.click(screen.getByText('Finalizza Montaggio'));
    
    // Verifica che le API siano state chiamate
    await waitFor(() => {
      expect(apiClient.updateMatches).toHaveBeenCalled();
      expect(apiClient.generateMontage).toHaveBeenCalledWith('test_job');
      expect(mockRouter.push).toHaveBeenCalledWith('/preview?jobId=test_job');
    });
  });
});

describe('PreviewPage', () => {
  beforeEach(() => {
    useSearchParams.mockReturnValue(new URLSearchParams('jobId=test_job'));
    apiClient.getDownloadUrl.mockResolvedValue({ download_url: '/api/download/test_job' });
  });
  
  test('renders preview page correctly', async () => {
    render(<PreviewPage />);
    
    // Verifica che la pagina di caricamento sia mostrata inizialmente
    expect(screen.getByText('Caricamento in corso...')).toBeInTheDocument();
    
    // Attendi che i dati simulati siano caricati
    await waitFor(() => {
      expect(screen.getByText('Anteprima del Montaggio')).toBeInTheDocument();
      expect(screen.getByText('Scarica Montaggio')).toBeInTheDocument();
      expect(screen.getByText('Riepilogo del Montaggio')).toBeInTheDocument();
    });
  });
  
  test('handles download', async () => {
    // Mock di window.open
    const originalOpen = window.open;
    window.open = jest.fn();
    
    render(<PreviewPage />);
    
    // Attendi che i dati simulati siano caricati
    await waitFor(() => {
      expect(screen.getByText('Scarica Montaggio')).toBeInTheDocument();
    });
    
    // Simula il clic sul pulsante di download
    fireEvent.click(screen.getByText('Scarica Montaggio'));
    
    // Verifica che il download sia iniziato
    expect(screen.getByText('Download in corso...')).toBeInTheDocument();
    
    // Ripristina window.open
    window.open = originalOpen;
  });
});
