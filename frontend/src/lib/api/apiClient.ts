// API client per la comunicazione con il backend
export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = '/api') {
    this.baseUrl = baseUrl;
  }

  // Verifica lo stato del backend
  async checkHealth(): Promise<any> {
    try {
      const response = await fetch(`${this.baseUrl}/health`);
      return await response.json();
    } catch (error) {
      console.error('Errore durante il controllo dello stato del backend:', error);
      throw error;
    }
  }

  // Carica un video e un riassunto
  async uploadVideo(videoFile: File, summary: string): Promise<any> {
    try {
      const formData = new FormData();
      formData.append('video', videoFile);
      formData.append('summary', summary);

      const response = await fetch(`${this.baseUrl}/upload`, {
        method: 'POST',
        body: formData,
      });

      return await response.json();
    } catch (error) {
      console.error('Errore durante il caricamento del video:', error);
      throw error;
    }
  }

  // Elabora un video caricato
  async processVideo(jobId: string): Promise<any> {
    try {
      const response = await fetch(`${this.baseUrl}/process/${jobId}`, {
        method: 'POST',
      });

      return await response.json();
    } catch (error) {
      console.error('Errore durante l\'elaborazione del video:', error);
      throw error;
    }
  }

  // Aggiorna le corrispondenze tra scene e frasi
  async updateMatches(jobId: string, matches: any[]): Promise<any> {
    try {
      const response = await fetch(`${this.baseUrl}/matches/${jobId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ matches }),
      });

      return await response.json();
    } catch (error) {
      console.error('Errore durante l\'aggiornamento delle corrispondenze:', error);
      throw error;
    }
  }

  // Genera il montaggio finale
  async generateMontage(jobId: string): Promise<any> {
    try {
      const response = await fetch(`${this.baseUrl}/generate/${jobId}`, {
        method: 'POST',
      });

      return await response.json();
    } catch (error) {
      console.error('Errore durante la generazione del montaggio:', error);
      throw error;
    }
  }

  // Ottiene l'URL di download del montaggio
  async getDownloadUrl(jobId: string): Promise<any> {
    try {
      const response = await fetch(`${this.baseUrl}/download/${jobId}`);
      return await response.json();
    } catch (error) {
      console.error('Errore durante il recupero dell\'URL di download:', error);
      throw error;
    }
  }
}

export default new ApiClient();
