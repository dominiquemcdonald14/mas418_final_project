library(tidyverse)

setwd("/Users/tixradmin/Documents/GitHub/mas418_final_project/Glassdoor")
job_data <- read.csv("jobs_glassdoor_dataset.csv")

setwd("/Users/tixradmin/Documents/GitHub/mas418_final_project/Glassdoor/Clean_R_Danny")

### Need to clean salary
salary_data <- job_data %>%
  filter(!is.na(company_salary))

str_extract_all("Employer est.:$78K - $162K ", "[0-9]+")

for (i in 1:nrow(salary_data)) {
  temp <- str_extract_all(salary_data$company_salary[i], "[0-9]+")[[1]]
  
  if (length(temp) == 2) {
    salary_temp <- mean(as.numeric(temp))
  } else {
    salary_temp <- as.numeric(temp)
  }
  
  salary_data$salary[i] <- salary_temp
}

write.csv(salary_data, "salary.csv")

### Next find the roles
### Role
### Level
role <- c("Data Scientist", "Data Analytics", "Applied Scientist",
          "Data Engineer", "Software Engineer", "Data Integration",
          "Machine Learning", "Systems Engineer", "Business Analytics",
          "Statistician", "Data Science", "Data Analyst")
role_change <- c("Data Scientist", "Data Analyst", "Machine Learning",
                 "Data Engineer", "Others", "Others",
                 "Machine Learning", "Others", "Data Analyst",
                 "Data Scientist", "Data Scientist", "Data Analyst")

for (i in 1:nrow(salary_data)) {
  temp <- salary_data$company_offeredRole[i]
  role_temp <- role_change[str_detect(temp, role)]
  
  salary_data$role[i] <- role_temp
}

table(salary_data$role)
write.csv(salary_data, "salary.csv")

check <- salary_data %>%
  filter(role %in% c("Machine Learning", "Applied Scientist"))
