# AAAD-Senior-Center-Profiles  

Senior Center Profile Updates  

Server Location: G:\3-GitHub Repository Folder Homes\Senior Center Updates

We have Senior Center profiles created on MySidewalk for every senior center that GNRC works with in our region. Marilyn will send out a request to have these updated, usually in the fall. Note that we would not be able to build these from scratch again on MySidewalk because since they were created, the size of data features allowed on a single profile was limited. These were grandfathered in. For this reason, I never delete pages, even those for centers that are non-operational, in case we get another center in the future and we would just need to change the geographies etc. Each one is made up of 5 links (size limitations) and you can see the annual update checklist I started to keep in 2023 in this folder called “Update Log.xlsx”. The profiles in MySidewalk are under the folder “Senior Center Profiles”. You can see the numbering system in Update Log that will allow you to search and open all pages of one profile at once for editing.   

Each profile has the following:
+ Main Page  
+ Demographics  
+ Senior Demographics  
+ Quality of Life  
+ Digital Profile  

The first thing will be examining the list that Marilyn sends. Check if the addresses are the same, if the names are the same, the website links are the same, if there are any that are no longer operational and don’t need to be updated, or if there are new ones. If there’s been a change of address that alters the radii then adjust accordingly. If there’s been a change of name then make sure that this is reflected in the profiles. The name change will affect the headline of each profile page, as well as the custom geography names. I have attempted to take the name out of any other part of the profiles for ease of updates.  


The next thing will be updating the information that MySidewalk doesn’t have. This is foreign born population on the demographics page, senior veterans on the senior demographics page, and transit access on the quality of life page. There are notebooks for each of these that are a bit old and clunky but they do the trick.   
 

Foreign Born Population:
This is on the Demographics page. The foreign born one calls directly to the Census API so if this is performed by other staff at some point you’ll need your own API key to run it. I really just take the percent of the county population that is foreign born from the notebook itself, and then use the output spreadsheets to list the top two or three places this population is born. Make sure to update the citation as well.  


Senior Veteran Population:
This is on the Senior Demographics Page. This calls to the Census Bureau SQLite database so make sure to update that to the newest vintage. This will output a spreadsheet at the county level that you use to update the info – make sure to update the citation.  


Transit Access:
This is on the Quality of Life Page. Go here: AllTransit, and select “Explore the AllTransit Map and Metrics”. Input the county and find the stats on the page for update.  

Everything else should update automatically with MySidewalks’s own system updates. The links stay the same.  
