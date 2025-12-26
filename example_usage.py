#!/usr/bin/env python3
"""
Beispiele für die programmgesteuerte Nutzung des Internetgeschwindigkeits-Rechners
"""

from internet_speed_calculator import InternetSpeedCalculator, SpeedUnit, SizeUnit


def example_speed_conversion():
    """Beispiel: Geschwindigkeitsumrechnung"""
    print("=" * 60)
    print("BEISPIEL 1: Geschwindigkeitsumrechnung")
    print("=" * 60)

    calculator = InternetSpeedCalculator()

    # Beispiel 1: Von Mbit/s zu MB/s
    mbit = 100
    mbyte = calculator.convert_speed(mbit, SpeedUnit.MBIT_S, SpeedUnit.MB_S)
    print(f"\n{mbit} Mbit/s = {mbyte} MB/s")

    # Beispiel 2: Von KB/s zu Mbit/s
    kb_s = 1250
    mbit_s = calculator.convert_speed(kb_s, SpeedUnit.KB_S, SpeedUnit.MBIT_S)
    print(f"{kb_s} KB/s = {mbit_s} Mbit/s")

    # Beispiel 3: Alle Einheiten anzeigen
    print(f"\nAlle Umrechnungen für 50 Mbit/s:")
    results = calculator.convert_all_units(50, SpeedUnit.MBIT_S)
    for unit, value in results.items():
        print(f"  {value:,.2f} {unit.value}")


def example_download_time():
    """Beispiel: Download-Zeit-Berechnung"""
    print("\n" + "=" * 60)
    print("BEISPIEL 2: Download-Zeit-Berechnung")
    print("=" * 60)

    calculator = InternetSpeedCalculator()

    # Beispiel 1: 4K Film (50 GB) bei 100 Mbit/s
    days, hours, minutes, seconds = calculator.calculate_download_time(
        50, SizeUnit.GB,
        100, SpeedUnit.MBIT_S
    )
    print(f"\n4K Film (50 GB) bei 100 Mbit/s:")
    print(f"  {hours} Stunden, {minutes} Minuten, {seconds} Sekunden")

    # Beispiel 2: Spiel-Update (15 GB) bei 50 Mbit/s
    days, hours, minutes, seconds = calculator.calculate_download_time(
        15, SizeUnit.GB,
        50, SpeedUnit.MBIT_S
    )
    total_minutes = hours * 60 + minutes
    print(f"\nSpiel-Update (15 GB) bei 50 Mbit/s:")
    print(f"  Etwa {total_minutes} Minuten")

    # Beispiel 3: Foto (5 MB) bei 16 Mbit/s
    days, hours, minutes, seconds = calculator.calculate_download_time(
        5, SizeUnit.MB,
        16, SpeedUnit.MBIT_S
    )
    print(f"\nFoto (5 MB) bei 16 Mbit/s:")
    print(f"  Etwa {seconds} Sekunden")


def example_comparison():
    """Beispiel: Vergleich verschiedener Internetgeschwindigkeiten"""
    print("\n" + "=" * 60)
    print("BEISPIEL 3: Vergleich verschiedener Geschwindigkeiten")
    print("=" * 60)

    calculator = InternetSpeedCalculator()

    file_size = 10  # GB
    speeds = [16, 50, 100, 250, 500, 1000]  # Mbit/s

    print(f"\nDownload von {file_size} GB bei verschiedenen Geschwindigkeiten:\n")
    print(f"{'Geschwindigkeit':<20} {'Download-Zeit':<30}")
    print("-" * 50)

    for speed in speeds:
        days, hours, minutes, seconds = calculator.calculate_download_time(
            file_size, SizeUnit.GB,
            speed, SpeedUnit.MBIT_S
        )

        # Formatiere die Ausgabe
        if hours > 0:
            time_str = f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            time_str = f"{minutes}m {seconds}s"
        else:
            time_str = f"{seconds}s"

        print(f"{speed} Mbit/s {'':<12} {time_str}")


def example_real_world():
    """Beispiel: Realistische Szenarien"""
    print("\n" + "=" * 60)
    print("BEISPIEL 4: Realistische Szenarien")
    print("=" * 60)

    calculator = InternetSpeedCalculator()

    scenarios = [
        ("Netflix 4K Stream (25 Mbit/s benötigt)", 25, SpeedUnit.MBIT_S),
        ("Zoom Video Call HD (3 Mbit/s benötigt)", 3, SpeedUnit.MBIT_S),
        ("Online Gaming (1 Mbit/s benötigt)", 1, SpeedUnit.MBIT_S),
        ("Musik Streaming (320 kbit/s benötigt)", 320, SpeedUnit.KBIT_S),
    ]

    print("\nMindestgeschwindigkeiten für verschiedene Aktivitäten:\n")

    for description, speed, unit in scenarios:
        # Konvertiere zu Mbit/s und MB/s für bessere Vergleichbarkeit
        mbit_s = calculator.convert_speed(speed, unit, SpeedUnit.MBIT_S)
        mb_s = calculator.convert_speed(speed, unit, SpeedUnit.MB_S)

        print(f"{description}")
        print(f"  {mbit_s:.2f} Mbit/s ({mb_s:.2f} MB/s)")

        # Berechne Datenverbrauch pro Stunde
        days, hours, minutes, seconds = calculator.calculate_download_time(
            1, SizeUnit.GB,
            speed, unit
        )
        total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds

        if total_seconds > 0:
            gb_per_hour = 3600 / total_seconds
            print(f"  Datenverbrauch: ~{gb_per_hour:.2f} GB/Stunde\n")


def example_unit_understanding():
    """Beispiel: Verständnis der Einheiten"""
    print("\n" + "=" * 60)
    print("BEISPIEL 5: Einheiten verstehen")
    print("=" * 60)

    calculator = InternetSpeedCalculator()

    print("\nWarum ist mein Download langsamer als meine Internetgeschwindigkeit?\n")

    internet_speed = 100  # Mbit/s (vom Internetanbieter)
    download_speed = calculator.convert_speed(internet_speed, SpeedUnit.MBIT_S, SpeedUnit.MB_S)

    print(f"Internetanbieter verspricht: {internet_speed} Mbit/s")
    print(f"Tatsächliche Download-Geschwindigkeit: {download_speed} MB/s")
    print(f"\nErklärung: 1 Byte = 8 Bits")
    print(f"Daher: {internet_speed} Mbit/s ÷ 8 = {download_speed} MB/s")

    print("\n" + "-" * 60)
    print("Häufige Verwirrungen:")
    print("-" * 60)

    confusions = [
        (100, SpeedUnit.MBIT_S, "Was der Anbieter verspricht"),
        (12.5, SpeedUnit.MB_S, "Was der Browser anzeigt"),
        (10, SpeedUnit.MB_S, "Was du real bekommst (wegen Overhead)"),
    ]

    for value, unit, description in confusions:
        bits = calculator.convert_speed(value, unit, SpeedUnit.BIT_S)
        mbits = bits / 1_000_000
        mbytes = calculator.convert_speed(value, unit, SpeedUnit.MB_S)

        print(f"\n{description}:")
        print(f"  {value} {unit.value}")
        print(f"  = {mbits:.2f} Mbit/s")
        print(f"  = {mbytes:.2f} MB/s")


def main():
    """Führt alle Beispiele aus"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "INTERNETGESCHWINDIGKEITS-RECHNER" + " " * 16 + "║")
    print("║" + " " * 20 + "Beispiele zur Nutzung" + " " * 17 + "║")
    print("╚" + "═" * 58 + "╝")

    example_speed_conversion()
    example_download_time()
    example_comparison()
    example_real_world()
    example_unit_understanding()

    print("\n" + "=" * 60)
    print("Weitere Informationen: siehe README.md")
    print("Interaktive Nutzung: python3 internet_speed_calculator.py")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
