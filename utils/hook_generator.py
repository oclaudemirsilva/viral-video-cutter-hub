import os
import subprocess
import re
import asyncio
import tempfile
import edge_tts
from datetime import datetime

class HookGenerator:
    """
    HookGenerator follows modular design for creating intro scenes with AI voice.
    It encapsulates TTS generation, FFmpeg filtering, and video concatenation.
    """
    
    def __init__(self, logger=None):
        self.logger = logger or print
        self.ffmpeg_path = "ffmpeg"
        self.ffprobe_path = "ffprobe"
        
    def _log(self, message):
        self.logger(f"[HookGenerator] {message}")

    async def _generate_audio(self, text, output_path, voice="pt-BR-AntonioNeural"):
        """Generates high-quality AI voice using Edge-TTS."""
        self._log(f"Gerando voz para o hook: '{text[:30]}...'")
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        return output_path

    def _get_audio_duration(self, audio_path):
        """Gets duration of an audio file using ffprobe."""
        try:
            cmd = [
                self.ffprobe_path, "-v", "error", "-show_entries", 
                "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", 
                audio_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return float(result.stdout.strip())
        except Exception as e:
            self._log(f"Erro ao detectar duração do áudio: {e}")
            return 3.0 # Fallback

    def _create_hook_scene(self, input_video, audio_path, text, output_path, duration):
        """
        Creates a frozen frame video from the first frame of input_video,
        overlays yellow text on a white box, and adds the generated audio.
        """
        self._log(f"Criando cena de hook (duração: {duration:.2f}s)")
        
        # Format text to Uppercase and split into lines for readability
        words = text.upper().split()
        lines = []
        for i in range(0, len(words), 3):
            lines.append(" ".join(words[i:i+3]))
        
        # Build drawtext filters
        # Using a yellow-gold text (#FFD700) on a semi-transparent white box
        drawtext_filters = []
        start_y = "h/3"
        for i, line in enumerate(lines):
            escaped_text = line.replace(":", "\\:").replace("'", "'\\''")
            y_offset = i * 90
            drawtext_filters.append(
                f"drawtext=text='{escaped_text}':fontcolor=#FFD700:box=1:boxcolor=white@0.9:"
                f"boxborderw=15:fontsize=65:x=(w-text_w)/2:y={start_y}+{y_offset}"
            )
        
        filter_complex = ",".join(drawtext_filters)
        
        # Command to: freeze 1st frame, apply text, add audio, set duration
        cmd = [
            self.ffmpeg_path, "-y",
            "-i", input_video,
            "-i", audio_path,
            "-filter_complex", f"[0:v]trim=0:0.04,loop=-1:1:0,setpts=PTS-STARTPTS,{filter_complex}[v]",
            "-map", "[v]", "-map", "1:a",
            "-t", str(duration + 0.5), # Small buffer
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            output_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            self._log(f"FFmpeg Error: {e.stderr.decode()}")
            return False

    def process_clip(self, input_path, hook_text, output_path):
        """
        Main interface: generates hook and concatenates with original clip.
        High-level method with low coupling to internal implementations.
        """
        temp_audio = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
        temp_hook_vid = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
        
        try:
            # 1. Generate Voice
            asyncio.run(self._generate_audio(hook_text, temp_audio))
            duration = self._get_audio_duration(temp_audio)
            
            # 2. Create Hook Video
            if not self._create_hook_scene(input_path, temp_audio, hook_text, temp_hook_vid, duration):
                return input_path # Fallback to original if hook fails
            
            # 3. Concatenate (Hook + Original)
            # We use complex filter to ensure parameters (res, fps) match precisely
            self._log("Concatenando hook ao clipe principal...")
            concat_cmd = [
                self.ffmpeg_path, "-y",
                "-i", temp_hook_vid,
                "-i", input_path,
                "-filter_complex", "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]",
                "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-c:a", "aac", "-b:a", "192k",
                output_path
            ]
            subprocess.run(concat_cmd, check=True, capture_output=True)
            return output_path
            
        except Exception as e:
            self._log(f"FALHA NO HOOK: {e}. Mantendo clipe original.")
            return input_path
        finally:
            # Cleanup
            for f in [temp_audio, temp_hook_vid]:
                if os.path.exists(f):
                    os.unlink(f)

# Usage example (not executed when imported):
# generator = HookGenerator()
# generator.process_clip("video.mp4", "Texto do Gancho", "result.mp4")
