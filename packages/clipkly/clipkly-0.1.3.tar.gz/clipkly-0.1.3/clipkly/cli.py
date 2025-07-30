import argparse
import json
import os
import pathlib
import re
import shlex
import subprocess
import unicodedata
from datetime import datetime

import pandas as pd
from tqdm import tqdm


def main():
    VERSION = "0.1.3"

    parser = argparse.ArgumentParser(
        description="Recorta clips desde uno o dos videos según un archivo JSON.")
    parser.add_argument("--offset", type=float, default=0.0,
                        help="Offset (en segundos) solo para el video vertical")
    parser.add_argument("--horizontal", type=str,
                        help="Ruta al archivo de video horizontal (opcional)")
    parser.add_argument("--vertical", type=str,
                        help="Ruta al archivo de video vertical (opcional)")
    parser.add_argument("--json", type=str, default="clips.json",
                        help="Archivo JSON con la definición de los clips")
    parser.add_argument("--filter", type=str,
                        help="Filtrar clips por categoría (opcional)")
    parser.add_argument("--duracion", type=str, choices=[
                        "muy_corto", "ideal", "largo", "muy_largo"], help="Filtrar clips por duración clasificada (opcional)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Solo mostrar lo que se haría sin ejecutar FFmpeg")
    parser.add_argument("--version", "-v", action="store_true",
                        help="Mostrar versión y salir")
    args = parser.parse_args()

    if args.version:
        print(f"clipkly v{VERSION}")
        exit()

    OFFSET_SECONDS = args.offset
    VIDEO_H = args.horizontal
    VIDEO_V = args.vertical
    TIMECODES = args.json
    FILTER = args.filter
    DURACION = args.duracion
    DRY_RUN = args.dry_run

    ROOT_DIR = pathlib.Path("clips")
    OUT_H = ROOT_DIR / "horizontal"
    OUT_V = ROOT_DIR / "vertical"
    OUT_H.mkdir(parents=True, exist_ok=True)
    OUT_V.mkdir(parents=True, exist_ok=True)

    def slugify(text: str) -> str:
        text = unicodedata.normalize("NFKD", text)
        text = text.encode("ascii", "ignore").decode("ascii")
        text = re.sub(r"\W+", "_", text.lower())
        return re.sub(r"_+", "_", text[:40].strip("_")) or "clip"

    def hhmmss_to_sec(t: str) -> float:
        dt = datetime.strptime(
            t, "%H:%M:%S.%f") if "." in t else datetime.strptime(t, "%H:%M:%S")
        return dt.hour * 3600 + dt.minute * 60 + dt.second + dt.microsecond / 1e6

    def sec_to_hhmmss(seconds: float) -> str:
        s = max(0, seconds)
        h = int(s // 3600)
        m = int((s % 3600) // 60)
        s = s % 60
        return f"{h:02}:{m:02}:{s:06.3f}"

    with open(TIMECODES, encoding="utf-8") as f:
        raw_clips = json.load(f)

    clips = [c for c in raw_clips if not FILTER or c.get("category") == FILTER]

    def clasifica(segundos):
        if segundos <= 30:
            return "muy_corto"
        elif segundos <= 90:
            return "ideal"
        elif segundos <= 179:
            return "largo"
        else:
            return "muy_largo"

    if DURACION:
        clips = [
            c for c in clips
            if clasifica(hhmmss_to_sec(c["end"]) - hhmmss_to_sec(c["start"])) == DURACION
        ]

    excel_data = []
    for c in clips:
        duracion = round(hhmmss_to_sec(
            c["end"]) - hhmmss_to_sec(c["start"]), 2)
        excel_data.append({
            "slug": c.get("slug"),
            "titulo": c.get("titulo"),
            "descripcion": c.get("descripcion", ""),
            "feeling": c.get("feeling", ""),
            "category": c.get("category", ""),
            "start": c.get("start"),
            "end": c.get("end"),
            "duracion_segundos": duracion,
            "duracion_mmss": f"{int(duracion // 60)}:{int(duracion % 60):02}",
            "clasificacion_duracion": clasifica(duracion),
            "score": c.get("score", ""),
            "tags": c.get("tags", ""),
            "quote": c.get("quote", ""),
            "kewords_detected": c.get("kewords_detected", ""),
            "personas_mencionadas": c.get("personas_mencionadas", ""),
            "actionable_tip": c.get("actionable_tip", ""),
            "thumbnail_hint": c.get("thumbnail_hint", ""),
            "platform_fit": c.get("platform_fit", ""),
            "transcript_excerpt": c.get("transcript_excerpt", ""),
            "ia_notes": c.get("ia_notes", ""),
            "fecha_publicacion": "",
            "estado": "por_publicar",
            "used_in_publication": c.get("used_in_publication", ""),
        })

    df = pd.DataFrame(excel_data)
    df.to_excel(ROOT_DIR / "estado_clips.xlsx", index=False)

    if VIDEO_H:
        print("🎬 Procesando clips del video horizontal (sin offset)...")
        for i, c in enumerate(tqdm(clips, desc="Horizontal")):
            start = hhmmss_to_sec(c["start"])
            end = hhmmss_to_sec(c["end"])
            slug = slugify(c.get("slug", f"clip_{i:02d}"))
            out = str(OUT_H / f"{i:02d}_{slug}.mp4").replace("\\", "/")
            cmd = f'ffmpeg -y -hide_banner -loglevel error -ss {sec_to_hhmmss(start)} -to {sec_to_hhmmss(end)} -i "{VIDEO_H}" -c copy "{out}"'
            if DRY_RUN:
                print("[DRY RUN]", cmd)
            else:
                subprocess.run(cmd, shell=True, check=True)

    if VIDEO_V:
        print("🎬 Procesando clips del video vertical (con offset aplicado)...")
        for i, c in enumerate(tqdm(clips, desc="Vertical")):
            start = hhmmss_to_sec(c["start"]) - OFFSET_SECONDS
            end = hhmmss_to_sec(c["end"]) - OFFSET_SECONDS
            slug = slugify(c.get("slug", f"clip_{i:02d}"))
            out = str(OUT_V / f"{i:02d}_{slug}.mp4").replace("\\", "/")
            cmd = f'ffmpeg -y -hide_banner -loglevel error -ss {sec_to_hhmmss(start)} -to {sec_to_hhmmss(end)} -i "{VIDEO_V}" -c copy "{out}"'
            if DRY_RUN:
                print("[DRY RUN]", cmd)
            else:
                subprocess.run(cmd, shell=True, check=True)

    print("\n✅ ¡Listo! Clips generados:")
    if VIDEO_H:
        print("📁", OUT_H)
    if VIDEO_V:
        print("📁", OUT_V)
    print("🗂️  Archivo Excel:", ROOT_DIR / "estado_clips.xlsx")


if __name__ == "__main__":
    main()
