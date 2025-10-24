import subprocess
import textwrap

# Usamos el console-script instalado por el paquete,
# no "python -m markitdown" (que fallaba en hatch)
CLI = ["markitdown"]

def run_cli(args, cwd=None, input_bytes=None):
    proc = subprocess.run(
        args,
        cwd=cwd,               # hatch ya prepara el PATH; no hace falta cwd
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return (
        proc.returncode,
        proc.stdout.decode("utf-8", "ignore"),
        proc.stderr.decode("utf-8", "ignore"),
    )


def test_summary_flag_limits_lines(tmp_path):
    # archivo grande
    content = "\n".join([f"line {i}" for i in range(1, 200)])
    p = tmp_path / "big.txt"
    p.write_text(content, encoding="utf-8")

    # --summary con límite de 10 líneas no vacías
    code, out, err = run_cli(CLI + ["--summary", "--summary-lines", "10", str(p), "-x", "txt"])
    assert code == 0, err

    # Contabilizamos solo las líneas de contenido del cuerpo (las que empiezan con "line ")
    body_lines = [ln for ln in out.splitlines() if ln.strip().startswith("line ")]
    # Debe devolver exactamente 10 líneas de contenido
    assert len(body_lines) == 10
    # No debe aparecer la línea 11 en el resumen truncado
    assert "line 11" not in out
    # Nota: algunos formatos pueden agregar encabezados o líneas en blanco;
    # no exigimos "…" o "..." porque el CLI actual no lo emite al truncar.


def test_summary_flag_no_truncate_small_file(tmp_path):
    p = tmp_path / "small.txt"
    p.write_text(textwrap.dedent("""\
        Title
        =====

        short file
        end
    """), encoding="utf-8")

    # Sin summary vs con summary: en archivo chico deben ser iguales
    code1, out_full, err1 = run_cli(CLI + [str(p), "-x", "txt"])
    code2, out_sum,  err2 = run_cli(CLI + ["--summary", str(p), "-x", "txt"])
    assert code1 == 0, err1
    assert code2 == 0, err2
    assert out_sum.strip() == out_full.strip()
