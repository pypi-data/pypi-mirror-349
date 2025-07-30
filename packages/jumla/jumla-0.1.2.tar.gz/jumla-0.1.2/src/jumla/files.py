class Files:
    @staticmethod
    def write_to_file(filename: str, content: str, mode: str = "w", log=False) -> None:
        try:
            with open(filename, mode, encoding="utf-8") as file:
                file.write(content)
                if log:
                    print(f"[✓] Successfully wrote to {filename}")
        except Exception as e:
            if log:
                print(f"[✗] Error writing to file: {e}")
            ValueError(f"Error writing to file: {e}")
