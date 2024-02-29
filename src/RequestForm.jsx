import { useForm, Controller } from "react-hook-form";
import { LoadingButton } from "@mui/lab";
import AppCheckbox from "./AppCheckbox";
import axios from "axios";
import { useState } from "react";
import Typography from "@mui/material/Typography";
import { Box, Grid, TextField } from "@mui/material";
import { ColoredJsonViewer } from "./ColoredJsonViewer";
import PropTypes from "prop-types";

export default function RequestForm({ darkMode }) {
  const {
    control,
    handleSubmit,
    formState: { isSubmitting },
  } = useForm();

  const [jsonData, setJsonData] = useState({});

  async function handleSubmitData(data) {
    try {
      data.json_input1 = JSON.parse(data.json_input1);
      data.json_input2 = JSON.parse(data.json_input2);

      const response = await axios.post(
        "http://127.0.0.1:5000/process_data",
        data
      );
      setJsonData(response.data);
    } catch (error) {
      console.log(error);
    }
  }

  return (
    <Box sx={{ p: 4 }}>
      <form onSubmit={handleSubmit(handleSubmitData)}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Controller
              name="json_input1"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  label="Routing"
                  multiline
                  rows={5}
                  fullWidth
                  variant="outlined"
                  placeholder="Write your line's routing..."
                />
              )}
            />
          </Grid>
          <Grid item xs={12}>
            <Controller
              name="json_input2"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  label="Task"
                  multiline
                  rows={5}
                  fullWidth
                  variant="outlined"
                  placeholder="Write ticket's meta here..."
                />
              )}
            />
          </Grid>
          <Grid
            item
            justifyContent="space-between"
            alignItems="center"
            gap={2}
            display="none"
          >
            <Typography>Under development (dont press)</Typography>
            <AppCheckbox
              name="isStrict"
              label="Strict Routing"
              control={control}
            />
          </Grid>
        </Grid>
        <Box justifyContent="space-between" display="flex" sx={{ mt: 3 }}>
          <LoadingButton
            loading={isSubmitting}
            variant="contained"
            type="submit"
            color="primary"
          >
            Run Script
          </LoadingButton>
        </Box>
      </form>
      <Grid container sx={{ mt: 3 }}>
        <Grid item xs={12}>
          <ColoredJsonViewer jsonData={jsonData} darkMode={darkMode} />
        </Grid>
      </Grid>
    </Box>
  );
}

RequestForm.propTypes = {
  darkMode: PropTypes.any,
};
