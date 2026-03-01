import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [isDoorOpen, setIsDoorOpen] = useState(false);
  const [buildingsData, setBuildingsData] = useState([]);

  const toggleDoor = () => {
    setIsDoorOpen(!isDoorOpen);
  };

  useEffect(() => {
    fetch('/data.json')
      .then(response => response.json())
      .then(data => setBuildingsData(data))
      .catch(error => console.error('Error loading data:', error));
  }, []);

  const getBuildingImage = ({ building_picture, building_file } = {}) => {
    const imageFile = building_picture || building_file;
    if (!imageFile) return '/placeholder.svg';
    return imageFile.startsWith('./') ? imageFile.slice(1) : imageFile;
  };

  const primaryColor = '#EF7022';

  return (
    <div className="h-screen bg-white flex flex-col overflow-hidden">
      <header className="flex-none h-[10%] flex items-center justify-between px-8 border-b border-gray-200">
        <div className="flex items-center cursor-pointer" onClick={toggleDoor}>
          <img 
            src={isDoorOpen ? '/freeRoomsLogo.png' : '/freeroomsDoorClosed.png'} 
            alt="Freerooms" 
            className="h-10 w-auto"
          />
          <span className="ml-2 text-xl font-bold text-[#EF7022]">
            Freerooms
          </span>
        </div>

        <div className="flex items-center gap-2">
          <button className="p-2 border border-orange-200 rounded-md text-orange-500">
            <span className="material-icons">map</span>
          </button>
          <button className="p-2 border border-orange-200 rounded-md text-orange-500 ">
            <span className="material-icons">search</span>
          </button>
          <button className="p-2 border border-orange-200 rounded-md text-orange-500">
            <span className="material-icons">dark_mode</span>
          </button>
        </div>
      </header>

      <div className="flex-none h-[8%] bg-white border-b border-gray-200 flex items-center justify-between px-8">
        <button 
          className="px-5 py-2 rounded-md text-white font-medium transition-colors"
          style={{ background: primaryColor }}
        >
          Filter
        </button>
        <div className="flex-1 max-w-xl">
          <div className="relative">
            <span className="material-icons absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">search</span>
            <input
              type="text"
              placeholder="Search for a building..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500/50 focus:border-orange-500"
            />
          </div>
        </div>
        <button 
          className="px-5 py-2 rounded-md text-white font-medium"
          style={{ backgroundColor: primaryColor }}
        >
          Sort
        </button>
      </div>

      <div className="flex-1 overflow-auto p-6">
        <div className="grid grid-cols-5 gap-4">
          {buildingsData.map((building, index) => (
            <div 
              key={index}
              className="group relative rounded-xl overflow-hidden border border-gray-100 bg-gray-100 aspect-[4/5] flex flex-col justify-end"
            >
              <img 
                src={getBuildingImage(building)}
                alt={building.name}
                className="absolute inset-0 w-full h-full"
              />
              <div className="absolute top-3 right-3 bg-white px-3 py-1.5 rounded-full text-xs font-semibold flex items-center gap-2 shadow-sm z-10 text-gray-700">
                <span className="w-2.5 h-2.5 rounded-full bg-[#008000]"></span>
                {building.rooms_available} rooms available
              </div>
              <div className="relative p-1.5 m-2 mt-auto rounded-lg shadow-sm"
                   style={{ backgroundColor: primaryColor }}>
                <h2 className="text-white font-medium text-sm truncate">
                  {building.name}
                </h2>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
