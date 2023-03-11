library(tidyverse)

setwd("/Users/tixradmin/Documents/GitHub/mas418_final_project/Glassdoor/output")
job_data <- read.csv("output_.csv")

setwd("/Users/tixradmin/Documents/GitHub/mas418_final_project/Glassdoor/Clean_R_Danny")

### Get rid of duplicates
job_no_dup <- data.frame()
job_no_dup <- rbind(job_no_dup, job_data[1,])

for (i in 1:nrow(job_data)) {
  temp <- job_data[i,]
  
  check <- rbind(job_no_dup, temp) %>%
    select(-requested_url) %>%
    group_by(companyName, company_offeredRole, company_roleLocation, company_salary) %>%
    summarise(count = n())
  
  if (mean(check$count) == 1) {
    job_no_dup <- rbind(job_no_dup, job_data[i,])
  }
}

### Need to clean salary
job_data <- job_data %>%
  select(-requested_url)

salary_data <- job_data %>%
  filter(!is.na(company_salary))

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
          "Statistician", "Data Science", "Data Analyst",
          "System Technician", "Artificial Intelligence", "Decision Scientist",
          "Natural Language Processing", "Data Architect", "Modeling",
          "Data Review")
role_change <- c("Data Scientist", "Data Analyst", "Machine Learning",
                 "Data Engineer", "Others", "Others",
                 "Machine Learning", "Others", "Data Analyst",
                 "Data Scientist", "Data Scientist", "Data Analyst",
                 "Others", "Machine Learning", "Data Scientist",
                 "Machine Learning", "Data Engineer", "Data Scientist",
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
  mutate(R = ifelse(str_detect(listing_jobDesc, "R"), 1, 0),
         Python = ifelse(str_detect(listing_jobDesc, "Python"), 1, 0),
         SQL = ifelse(str_detect(listing_jobDesc, "SQL"), 1, 0))

sum(salary_data$R)/nrow(salary_data)
sum(salary_data$Python)/nrow(salary_data)
sum(salary_data$SQL)/nrow(salary_data)

write.csv(salary_data, "salary.csv")

