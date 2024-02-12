import { Checkbox, FormControlLabel } from "@mui/material";
import { useController } from "react-hook-form";

export default function AppCheckbox(props) {
  const { field } = useController({ ...props, defaultValue: false });
  return (
    <FormControlLabel
      control={<Checkbox {...field} checked={field.value} color="primary" />}
    />
  );
}