#!/usr/bin/env python3
"""
Internetgeschwindigkeits-Rechner
Konvertiert zwischen verschiedenen Einheiten und berechnet Download-Zeiten
"""

from enum import Enum
from typing import Dict, Tuple


class SpeedUnit(Enum):
    """Enum für Geschwindigkeitseinheiten"""
    BIT_S = "bit/s"
    KBIT_S = "Kbit/s"
    MBIT_S = "Mbit/s"
    GBIT_S = "Gbit/s"
    BYTE_S = "Byte/s"
    KB_S = "KB/s"
    MB_S = "MB/s"
    GB_S = "GB/s"


class SizeUnit(Enum):
    """Enum für Dateigrößen-Einheiten"""
    BYTE = "Byte"
    KB = "KB"
    MB = "MB"
    GB = "GB"
    TB = "TB"


class InternetSpeedCalculator:
    """Rechner für Internetgeschwindigkeiten"""

    # Konvertierungsfaktoren zu bit/s
    SPEED_TO_BITS = {
        SpeedUnit.BIT_S: 1,
        SpeedUnit.KBIT_S: 1_000,
        SpeedUnit.MBIT_S: 1_000_000,
        SpeedUnit.GBIT_S: 1_000_000_000,
        SpeedUnit.BYTE_S: 8,
        SpeedUnit.KB_S: 8_000,
        SpeedUnit.MB_S: 8_000_000,
        SpeedUnit.GB_S: 8_000_000_000,
    }

    # Konvertierungsfaktoren zu Bytes
    SIZE_TO_BYTES = {
        SizeUnit.BYTE: 1,
        SizeUnit.KB: 1_000,
        SizeUnit.MB: 1_000_000,
        SizeUnit.GB: 1_000_000_000,
        SizeUnit.TB: 1_000_000_000_000,
    }

    def convert_speed(self, value: float, from_unit: SpeedUnit, to_unit: SpeedUnit) -> float:
        """
        Konvertiert Geschwindigkeit von einer Einheit zur anderen

        Args:
            value: Geschwindigkeitswert
            from_unit: Quelleinheit
            to_unit: Zieleinheit

        Returns:
            Konvertierter Geschwindigkeitswert
        """
        # Erst zu bit/s konvertieren
        bits_per_second = value * self.SPEED_TO_BITS[from_unit]

        # Dann zur Zieleinheit konvertieren
        result = bits_per_second / self.SPEED_TO_BITS[to_unit]

        return result

    def convert_all_units(self, value: float, from_unit: SpeedUnit) -> Dict[SpeedUnit, float]:
        """
        Konvertiert einen Wert in alle verfügbaren Einheiten

        Args:
            value: Geschwindigkeitswert
            from_unit: Quelleinheit

        Returns:
            Dictionary mit allen Konvertierungen
        """
        results = {}
        for unit in SpeedUnit:
            results[unit] = self.convert_speed(value, from_unit, unit)
        return results

    def calculate_download_time(self, file_size: float, size_unit: SizeUnit,
                                speed: float, speed_unit: SpeedUnit) -> Tuple[int, int, int, int]:
        """
        Berechnet die Download-Zeit für eine Datei

        Args:
            file_size: Größe der Datei
            size_unit: Einheit der Dateigröße
            speed: Internetgeschwindigkeit
            speed_unit: Einheit der Geschwindigkeit

        Returns:
            Tuple mit (Tage, Stunden, Minuten, Sekunden)
        """
        # Konvertiere Dateigröße zu Bytes
        total_bytes = file_size * self.SIZE_TO_BYTES[size_unit]

        # Konvertiere Geschwindigkeit zu Bytes/Sekunde
        bytes_per_second = self.convert_speed(speed, speed_unit, SpeedUnit.BYTE_S)

        # Berechne Zeit in Sekunden
        total_seconds = total_bytes / bytes_per_second

        # Konvertiere zu Tagen, Stunden, Minuten, Sekunden
        days = int(total_seconds // 86400)
        remaining = total_seconds % 86400
        hours = int(remaining // 3600)
        remaining = remaining % 3600
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)

        return days, hours, minutes, seconds


def print_header(title: str):
    """Druckt einen formatierten Header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def get_speed_unit_choice() -> SpeedUnit:
    """Fragt den Benutzer nach einer Geschwindigkeitseinheit"""
    print("\nVerfügbare Einheiten:")
    units = list(SpeedUnit)
    for i, unit in enumerate(units, 1):
        print(f"  {i}. {unit.value}")

    while True:
        try:
            choice = int(input("\nWähle eine Einheit (Nummer): "))
            if 1 <= choice <= len(units):
                return units[choice - 1]
            else:
                print(f"Bitte wähle eine Nummer zwischen 1 und {len(units)}")
        except ValueError:
            print("Bitte gib eine gültige Nummer ein")


def get_size_unit_choice() -> SizeUnit:
    """Fragt den Benutzer nach einer Dateigrößen-Einheit"""
    print("\nVerfügbare Einheiten:")
    units = list(SizeUnit)
    for i, unit in enumerate(units, 1):
        print(f"  {i}. {unit.value}")

    while True:
        try:
            choice = int(input("\nWähle eine Einheit (Nummer): "))
            if 1 <= choice <= len(units):
                return units[choice - 1]
            else:
                print(f"Bitte wähle eine Nummer zwischen 1 und {len(units)}")
        except ValueError:
            print("Bitte gib eine gültige Nummer ein")


def speed_conversion_menu(calculator: InternetSpeedCalculator):
    """Menü für Geschwindigkeitsumrechnung"""
    print_header("GESCHWINDIGKEITSUMRECHNUNG")

    # Eingabewert
    while True:
        try:
            value = float(input("\nGeschwindigkeit eingeben: "))
            if value >= 0:
                break
            else:
                print("Bitte gib einen positiven Wert ein")
        except ValueError:
            print("Bitte gib eine gültige Zahl ein")

    # Eingabeeinheit
    print("\nVon welcher Einheit?")
    from_unit = get_speed_unit_choice()

    # Alle Umrechnungen anzeigen
    print(f"\n{value} {from_unit.value} entspricht:")
    print("-" * 60)

    results = calculator.convert_all_units(value, from_unit)

    # Gruppiere nach Bit- und Byte-Einheiten
    print("\nBit-basierte Einheiten:")
    for unit in [SpeedUnit.BIT_S, SpeedUnit.KBIT_S, SpeedUnit.MBIT_S, SpeedUnit.GBIT_S]:
        result = results[unit]
        print(f"  {result:,.2f} {unit.value}")

    print("\nByte-basierte Einheiten:")
    for unit in [SpeedUnit.BYTE_S, SpeedUnit.KB_S, SpeedUnit.MB_S, SpeedUnit.GB_S]:
        result = results[unit]
        print(f"  {result:,.2f} {unit.value}")


def download_time_menu(calculator: InternetSpeedCalculator):
    """Menü für Download-Zeit-Berechnung"""
    print_header("DOWNLOAD-ZEIT BERECHNEN")

    # Dateigröße eingeben
    while True:
        try:
            file_size = float(input("\nDateigröße eingeben: "))
            if file_size >= 0:
                break
            else:
                print("Bitte gib einen positiven Wert ein")
        except ValueError:
            print("Bitte gib eine gültige Zahl ein")

    print("\nEinheit der Dateigröße?")
    size_unit = get_size_unit_choice()

    # Geschwindigkeit eingeben
    while True:
        try:
            speed = float(input("\nInternetgeschwindigkeit eingeben: "))
            if speed > 0:
                break
            else:
                print("Bitte gib einen positiven Wert größer 0 ein")
        except ValueError:
            print("Bitte gib eine gültige Zahl ein")

    print("\nEinheit der Geschwindigkeit?")
    speed_unit = get_speed_unit_choice()

    # Berechne Download-Zeit
    days, hours, minutes, seconds = calculator.calculate_download_time(
        file_size, size_unit, speed, speed_unit
    )

    # Ergebnis anzeigen
    print("\n" + "=" * 60)
    print(f"  Download von {file_size} {size_unit.value} bei {speed} {speed_unit.value}")
    print("=" * 60)

    # Zeige nur relevante Zeiteinheiten
    time_parts = []
    if days > 0:
        time_parts.append(f"{days} Tag{'e' if days != 1 else ''}")
    if hours > 0 or days > 0:
        time_parts.append(f"{hours} Stunde{'n' if hours != 1 else ''}")
    if minutes > 0 or hours > 0 or days > 0:
        time_parts.append(f"{minutes} Minute{'n' if minutes != 1 else ''}")
    time_parts.append(f"{seconds} Sekunde{'n' if seconds != 1 else ''}")

    print(f"\nGeschätzte Download-Zeit: {', '.join(time_parts)}")

    # Zeige auch Gesamtzeit in verschiedenen Einheiten
    total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds
    print(f"\nOder:")
    if total_seconds >= 86400:
        print(f"  {total_seconds / 86400:.2f} Tage")
    if total_seconds >= 3600:
        print(f"  {total_seconds / 3600:.2f} Stunden")
    if total_seconds >= 60:
        print(f"  {total_seconds / 60:.2f} Minuten")
    print(f"  {total_seconds:.0f} Sekunden")


def quick_reference():
    """Zeigt eine Schnellreferenz für gängige Geschwindigkeiten"""
    print_header("SCHNELLREFERENZ")

    print("\nGängige Internetgeschwindigkeiten:")
    print("-" * 60)

    common_speeds = [
        (16, "DSL 16.000"),
        (50, "Kabel 50"),
        (100, "Glasfaser 100"),
        (250, "Glasfaser 250"),
        (500, "Glasfaser 500"),
        (1000, "Gigabit (1 Gbit/s)"),
    ]

    calculator = InternetSpeedCalculator()

    for speed_mbit, description in common_speeds:
        speed_mb = calculator.convert_speed(speed_mbit, SpeedUnit.MBIT_S, SpeedUnit.MB_S)
        print(f"\n{description}:")
        print(f"  {speed_mbit} Mbit/s = {speed_mb:.2f} MB/s")

        # Beispiel: 1 GB Download
        days, hours, minutes, seconds = calculator.calculate_download_time(
            1, SizeUnit.GB, speed_mbit, SpeedUnit.MBIT_S
        )
        total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds

        if total_seconds >= 60:
            print(f"  1 GB Download: ~{int(total_seconds / 60)} Minuten {int(total_seconds % 60)} Sekunden")
        else:
            print(f"  1 GB Download: ~{int(total_seconds)} Sekunden")


def main():
    """Hauptprogramm"""
    calculator = InternetSpeedCalculator()

    print("=" * 60)
    print("  INTERNETGESCHWINDIGKEITS-RECHNER")
    print("=" * 60)
    print("\n  Willkommen! Dieser Rechner hilft dir bei:")
    print("  - Umrechnung von Geschwindigkeitseinheiten")
    print("  - Berechnung von Download-Zeiten")
    print("  - Übersicht gängiger Internetgeschwindigkeiten")

    while True:
        print("\n" + "=" * 60)
        print("HAUPTMENÜ")
        print("=" * 60)
        print("\n1. Geschwindigkeit umrechnen")
        print("2. Download-Zeit berechnen")
        print("3. Schnellreferenz anzeigen")
        print("4. Beenden")

        choice = input("\nWähle eine Option (1-4): ")

        if choice == "1":
            speed_conversion_menu(calculator)
        elif choice == "2":
            download_time_menu(calculator)
        elif choice == "3":
            quick_reference()
        elif choice == "4":
            print("\nAuf Wiedersehen! 👋")
            break
        else:
            print("\nUngültige Auswahl. Bitte wähle 1-4.")


if __name__ == "__main__":
    main()
