import logo from "./logo.svg";
import "./App.css";
import { useState } from "react";
import axios from "axios";

function App() {
  const CITIES = [
    "United States,",
    "Austin,Tx",
    "Dallas,Tx",
    "Houston,Tx",
    "Detriot,Mi",
    "San Jose,Ca",
    "San Diego,Ca",
    "Chicago,Il",
    "San Francisco,Ca",
    "New York,Ny",
    "Newark,New Jersey",
    "Akron,Ohio",
    "Miami,Fl",
  ];
  const [cityName, setCityName] = useState("Austin,Tx");
  const [searchJob, setSearchJob] = useState(CITIES[0]);
  const [selectedOption, setSelectedOption] = useState("latest");
  const [jsonData, setJsonData] = useState([]);
  const [showData, setShowData] = useState(false);

  const [showLoadedDb, setShowLoadedDb] = useState(false);

  const onSubmit = (text) => async (event) => {
    event.preventDefault();
    console.log(searchJob + " in " + cityName);
    console.log(text);
    try {
      // Use axios.post instead of fetch
      const response = await axios.post("http://localhost:5001/api/get-data/", {
        title: searchJob + " in " + cityName, // Send the searchJob in the request body
        latest: selectedOption,
        type: text,
      });

      if (text === "Search") {
        setJsonData(JSON.parse(response.data));
        setShowData(true);
        setShowLoadedDb(false);
      }
      if (text === "Load") {
        setShowLoadedDb(true);
        setShowData(false);
      }
    } catch (error) {
      console.error(error);
    }
  };

  const applyJob = async (link, job_id) => {
    const filteredJobs = jsonData.filter((item) => item.job_id !== job_id);
    setJsonData(filteredJobs);
    window.open(link, "_blank");
    axios.post("http://localhost:5001/api/apply-id/", {
      job_id: job_id,
    });
  };

  const removeJob = async (job_id) => {
    const filteredJobs = jsonData.filter((item) => item.job_id !== job_id);
    setJsonData(filteredJobs);
    axios.post("http://localhost:5001/api/remove-id/", {
      job_id: job_id,
    });
  };
  return (
    <div className="App">
      Hey, Rahul let's see if this works out!
      <form>
        <div className="search">
          <div className="horizontal">
            <input
              type="text"
              placeholder="Enter Job role"
              onChange={(e) => {
                setSearchJob(e.target.value);
              }}
            />
            <input
              type="submit"
              value="Search DB"
              onClick={onSubmit("Search")}
            />
            <input type="submit" value="Load DB" onClick={onSubmit("Load")} />
          </div>
          <div className="horizontal">
            <select
              value={cityName}
              onChange={(e) => {
                setCityName(e.target.value);
              }}
            >
              {CITIES.map((city, index) => (
                <option key={index} value={city}>
                  {city}
                </option>
              ))}
            </select>
            <label>
              <input
                type="radio"
                name="option"
                value="latest"
                checked={selectedOption === "latest"}
                onChange={(e) => {
                  setSelectedOption(e.target.value);
                }}
              />
              Latest
            </label>
            <label>
              <input
                type="radio"
                name="option"
                value="old"
                checked={selectedOption === "old"}
                onChange={(e) => {
                  setSelectedOption(e.target.value);
                }}
              />
              Old
            </label>
          </div>
        </div>
      </form>
      {showData ? (
        <table>
          <thead>
            <tr>
              <th>Job Title</th>
              <th>Employer</th>
              <th>Quality Score</th>
              <th>Date Posted</th>
              <th>Job Link</th>
              <th>Remove Job</th>
            </tr>
          </thead>
          <tbody>
            {jsonData.map((item) => (
              <tr key={item.job_id}>
                <td>{item.job_title}</td>
                <td>{item.employer_name}</td>
                <td>{item.job_apply_quality_score}</td>
                <td>{item.job_posted_at_datetime_utc}</td>
                <td>
                  <button
                    onClick={() => {
                      applyJob(item.job_apply_link, item.job_id);
                    }}
                  >
                    Link
                  </button>
                </td>
                <td>
                  <button
                    onClick={() => {
                      removeJob(item.job_id);
                    }}
                  >
                    Remove
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : showLoadedDb ? (
        <div> Loaded 10 records</div>
      ) : (
        <div>No Data please search</div>
      )}
    </div>
  );
}

export default App;
