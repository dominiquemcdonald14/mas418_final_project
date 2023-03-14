library(tidyverse)

setwd("/Users/tixradmin/Documents/GitHub/mas418_final_project/Glassdoor/output")
job_data <- read.csv("output_no_dup.csv")

setwd("/Users/tixradmin/Documents/GitHub/mas418_final_project/Danny/Clean_R_Danny")
job_data <- read.csv("salary_no_dup.csv")

### Cleaning up, first salary
salary_data <- job_data %>%
  filter(!is.na(company_salary))
index <- which(salary_data$companyName == "companyName")
salary_data <- salary_data[-index,]

for (i in 1:nrow(salary_data)) {
  
  if (str_detect(salary_data$company_salary[i],"Hour")) {
    temp <- str_extract_all(salary_data$company_salary[i], "\\$[0-9]+")[[1]]
    temp_new <- substr(temp, 2, nchar(temp))
    
    if (length(temp) == 2) {
      salary_temp <- mean(as.numeric(temp_new))
    } else {
      salary_temp <- as.numeric(temp_new)
    } 
    
  } else {
    temp <- str_extract_all(salary_data$company_salary[i], "[0-9]+")[[1]]
    
    if (length(temp) == 2) {
      salary_temp <- mean(as.numeric(temp))
    } else {
      salary_temp <- as.numeric(temp)
    } 
  }
  
  salary_data$salary[i] <- salary_temp
}

### Next find the roles
### Role
### Level
role <- c("Data Scientist", "Data Analytics", "Applied Scientist",
          "Data Engineer", "Software Engineer", "Data Integration",
          "Machine Learning", "Systems Engineer", "Business Analytics",
          "Statistician", "Data Science", "Data Analyst",
          "System Technician", "Artificial Intelligence", "Decision Scientist",
          "Natural Language Processing", "Data Architect", "Modeling",
          "Data Review", "Reporting Analyst", "AI Architect",
          "Statistical Program", "AI", "Mathematician",
          "Data Quality Engineer", "Predictive Analytics Modeler", "Deep Learning",
          "Data Management Analyst")
role_change <- c("Data Scientist", "Data Analyst", "Machine Learning",
                 "Data Engineer", "Others", "Others",
                 "Machine Learning", "Others", "Data Analyst",
                 "Data Scientist", "Data Scientist", "Data Analyst",
                 "Others", "Machine Learning", "Data Scientist",
                 "Machine Learning", "Data Engineer", "Data Scientist",
                 "Data Analyst", "Data Analyst", "Machine Learning",
                 "Data Scientist", "Machine Learning", "Others",
                 "Data Engineer", "Data Scientist", "Machine Learning",
                 "Data Analyst")

for (i in 1:nrow(salary_data)) {
  temp <- salary_data$company_offeredRole[i]
  role_temp <- role_change[str_detect(temp, role)]
  
  salary_data$role[i] <- role_temp
}

table(salary_data$role)

### Next location
for (i in 1:nrow(salary_data)) {
  temp <- salary_data$company_roleLocation[i]
  num <- nchar(temp)
  
  if (temp == "Remote") {
    salary_data$location[i] <- "Remote"
  } else {
    salary_data$location[i] <- substr(temp, num-1, num)
  }
}

table(salary_data$location)

### Also Skills
salary_data <- salary_data %>%
  mutate(#R = ifelse(str_detect(listing_jobDesc, "R"), 1, 0),
         Python = ifelse(str_detect(listing_jobDesc, "Python"), 1, 0),
         SQL = ifelse(str_detect(listing_jobDesc, "SQL"), 1, 0))

#sum(salary_data$R)/nrow(salary_data)
sum(salary_data$Python)/nrow(salary_data)
sum(salary_data$SQL)/nrow(salary_data)

### Let's add education
salary_data <- salary_data %>%
  mutate(PhD = ifelse(str_detect(listing_jobDesc, "PhD") | str_detect(listing_jobDesc, "Ph. D") | str_detect(listing_jobDesc, "Doctoral"), "PhD", "None"),
         Master = ifelse(str_detect(listing_jobDesc, "Master") | str_detect(listing_jobDesc, "MS"), "Master","None"),
         Bachelor = ifelse(str_detect(listing_jobDesc, "Bachelor") | str_detect(listing_jobDesc, "BA") | str_detect(listing_jobDesc, "bachelor"), "Bachelor","None"))

sum(salary_data$PhD == "PhD")
sum(salary_data$Master == "Master")
sum(salary_data$Bachelor == "Bachelor")

salary_data <- salary_data %>%
  mutate(High_Ed = ifelse(str_detect(PhD, "PhD"), "PhD", 
                      ifelse(str_detect(Master, "Master"), "Master",
                        ifelse(str_detect(Bachelor, "Bachelor"), "Bachelor","None"))))


setwd("/Users/tixradmin/Documents/GitHub/mas418_final_project/Danny/Clean_R_Danny")

write.csv(salary_data, "salary.csv")
