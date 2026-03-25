import os
import re
import json
import subprocess
import time
from i18n.i18n import I18nAuto

i18n = I18nAuto()

class StyleEngine:
    def __init__(self, project_folder=None):
        self.project_folder = project_folder
        self.style_description = "Cinematic, high quality, consistent lighting."
        
    def analyze_references(self, image_paths):
        """
        Analyzes reference images to create a 'style prompt' to be appended 
        to all future generation requests.
        (Placeholder for Vision LLM logic)
        """
        print(i18n("Analyzing style references..."))
        if not image_paths:
            return self.style_description
        
        # Real logic would use Gemini Vision or CLIP to describe the style
        # For now, we simulate a 'detected style'
        detected_style = "Vibrant colors, high contrast, minimalist, clean lines."
        self.style_description = detected_style
        return detected_style

    def generate_image_prompts(self, viral_segments):
        """
        Processes viral segments and determines where B-roll images should be placed.
        Returns a list of dicts: {'timestamp': 10.5, 'prompt': '...'}
        """
        print(i18n("Generating B-roll image prompts based on transcript..."))
        prompts = []
        
        segments = viral_segments.get("segments", [])
        for i, seg in enumerate(segments):
            # Extract key concepts from text
            text = seg.get("text", "")
            # Simple heuristic: Pick sentences with strong visual words
            # Real logic would use LLM to pick best moments
            prompt = f"{text}. {self.style_description}"
            prompts.append({
                "segment_idx": i,
                "timestamp": 2.0, # 2 seconds into the clip
                "duration": 3.0,
                "prompt": prompt
            })
            
        return prompts

    def generate_broll_images(self, prompts):
        """
        Calls an Image Gen API to create the images.
        (Mock version using FFmpeg to create placeholders for testing)
        """
        print(i18n("Generating AI Images (B-Roll)..."))
        generated_images = []
        
        broll_folder = os.path.join(self.project_folder, "broll")
        os.makedirs(broll_folder, exist_ok=True)
        
        for i, item in enumerate(prompts):
            img_path = os.path.join(broll_folder, f"broll_{i:03d}.png")
            print(f"   🖼️ Gerando imagem para: {item['prompt'][:50]}...")
            
            # Simple placeholder image with prompt text using FFmpeg
            safe_prompt = item['prompt'][:80].replace("'", "").replace(":", "")
            # Split text into lines for visibility
            lines = [safe_prompt[i:i+20] for i in range(0, len(safe_prompt), 20)]
            display_text = "\\n".join(lines)
            
            cmd = [
                "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=purple:s=1080x1920:d=1",
                "-vf", f"drawtext=text='[AI B-ROLL]\\n{display_text}':fontcolor=white:fontsize=40:x=(w-text_w)/2:y=(h-text_h)/2",
                "-frames:v", "1", img_path
            ]
            subprocess.run(cmd, capture_output=True)
            
            if os.path.exists(img_path):
                generated_images.append({'path': img_path, 'item': item})
            
        return generated_images

    def process_broll_for_clip(self, video_path, clip_idx, broll_plan):
        """
        Overlays multiple B-roll images on a single clip.
        """
        temp_out = video_path.replace(".mp4", "_broll_tmp.mp4")
        current_in = video_path
        
        # Filter plan for this specific clip
        clip_prompts = [p for p in broll_plan if p['segment_idx'] == clip_idx]
        
        if not clip_prompts:
            return video_path
            
        # Generate images for these prompts
        images = self.generate_broll_images(clip_prompts)
        
        for i, img_data in enumerate(images):
            img_p = img_data['path']
            ts = img_data['item']['timestamp']
            dur = img_data['item']['duration']
            
            out_p = video_path.replace(".mp4", f"_broll_step_{i}.mp4")
            
            success = self.overlay_broll(current_in, img_p, ts, dur, out_p)
            if success:
                if current_in != video_path and os.path.exists(current_in):
                    os.remove(current_in)
                current_in = out_p
            else:
                print(f"   ❌ Erro ao sobrepor B-Roll {i}")
                
        if current_in != video_path:
            os.replace(current_in, video_path)
            print(f"   ✅ B-Roll aplicado no clipe {clip_idx}")
            
        return video_path

    def overlay_broll(self, video_path, image_path, start_time, duration, output_path):
        """
        Uses FFmpeg to overlay an image over a video for a specific duration.
        """
        print(f"   🎬 Aplicando sobreposição de B-Roll: {start_time}s")
        
        # overlay=0:0 (Full screen) or centered.
        # We also want a fade in/out effect for 'Premium' feel.
        fade_in = 0.5
        fade_out = 0.5
        
        # FFmpeg filter: scale, fade, overlay
        filter_complex = (
            f"[1:v]scale=1080:-1,format=rgba,"
            f"fade=t=in:st=0:d={fade_in}:alpha=1,"
            f"fade=t=out:st={duration-fade_out}:d={fade_out}:alpha=1[img];"
            f"[0:v][img]overlay=0:0:enable='between(t,{start_time},{start_time+duration})'"
        )
        
        cmd = [
            "ffmpeg", "-y", "-i", video_path, "-i", image_path,
            "-filter_complex", filter_complex,
            "-codec:a", "copy", output_path
        ]
        
        res = subprocess.run(cmd, capture_output=True, text=True)
        return res.returncode == 0
