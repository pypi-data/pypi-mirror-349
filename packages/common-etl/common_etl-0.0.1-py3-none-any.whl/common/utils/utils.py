import pandas as pd


class RemoveLeadingZeros:

    def remove_leading_zeros(self, val):
        try:
            # Check if the value is a date
            pd.to_datetime(val, format="%d.%m.%Y", errors="raise")
            return val
        except ValueError:
            # If not a date, proceed with removing leading zeros
            val_str = str(val)
            if val_str.startswith("-"):
                val_str = "-" + val_str.lstrip("-0")
            else:
                val_str = val_str.lstrip("0")

            if val_str == "" or val_str == ".":
                return "0"
            elif "." in val_str and "e" not in val_str and "E" not in val_str:
                try:
                    return "{:.2f}".format(float(val_str))
                except ValueError:
                    pass  # If conversion fails, keep the original value
            elif "e" in val_str or "E" in val_str:
                try:
                    return "{:.2e}".format(float(val_str))
                except ValueError:
                    pass  # If conversion fails, keep the original value
            return val_str


class RemoveLeadingZeroForMaterial:

    def remove_leading_zeros_for_material(self, number):
        # Remove leading zeros but keep one zero if the number starts with zero
        number = number.lstrip('0')
        if number == '':
            return '0'
        return number.zfill(8)
