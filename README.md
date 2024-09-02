# National-Park-Service-NPS

## Background 

The National Park Service (NPS) manages a vast array of natural and cultural sites across the United States, from the iconic Yellowstone National Park to the historic Gettysburg National Battlefield. To provide developers, researchers, and park enthusiasts with easy access to essential information about these sites, the NPS offers a robust API (Application Programming Interface). This API serves as a one-stop shop for retrieving data such as photos, visitor center information, campgrounds, events, news alerts, and articles on natural and cultural features.

In this project, my focus is on two key aspects: <br/>
	1.	Harvesting Parking Fee Data: Extracting detailed information on parking fees for various types of NPS sites, including National Parks, National Memorials, National Scenic Trails, National Battlefields, National Monuments, National Rivers, National Reserves, and National Recreation Areas. <br/>
	2.	Data Visualization: Using Tableau to visualize the harvested data, making it easier to identify patterns, compare fees across different sites, and gain insights into the NPS’s fee structures.

## Key Fields/Features Extracted

For this project, the following fields have been extracted from the NPS API:
	•	ParkCode: A unique identifier for each park.<br/>
	•	State: The state(s) in which the park is located.<br/>
	•	Name of the National Park: The official name of the park.<br/>
	•	Type of the National Park (Designation): The designation of the park (e.g., National Park, National Monument).<br/>
	•	Latitude: The geographic latitude of the park.<br/>
	•	Longitude: The geographic longitude of the park.<br/>
	•	LatLong: A combined field of latitude and longitude.<br/>
	•	Fee USD: The parking fee in U.S. dollars.<br/>
	•	Fee Type: The type of fee (e.g., per vehicle, per person).<br/>
	•	Fee Description: A brief description of what the fee covers.<br/>



## Visualize the harvested data in Tableau

[Link to Live Tableau Public Dashboard ](https://public.tableau.com/views/NATIONALPARKSERVICE/NATIONALPARKSERVICE?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

![Image1](https://github.com/gagandeepsinghkhanuja/National-Park-Service-NPS/blob/main/Output/NPS%20-%20By%20State.png)

![Image2](https://github.com/gagandeepsinghkhanuja/National-Park-Service-NPS/blob/main/Output/NPS%20Entry%20Fee%20-%20By%20Vehicle%20Type.png)


API Guidebook:
https://www.nps.gov/subjects/developer/guides.htm

API Endpoints and Description
https://www.nps.gov/subjects/developer/api-documentation.htm
