library(tidyverse)
library(modelr)

df <- read_csv("nst-est2018-alldata.csv", col_names=TRUE,
               col_types=cols_only(
                  NAME = "c",
                  POPESTIMATE2010 = "i",
                  POPESTIMATE2011 = "i",
                  POPESTIMATE2012 = "i",
                  POPESTIMATE2013 = "i",
                  POPESTIMATE2014 = "i",
                  POPESTIMATE2015 = "i",
                  POPESTIMATE2016 = "i",
                  POPESTIMATE2017 = "i",
                  POPESTIMATE2018 = "i")
               )

df <- df %>% 
  filter(NAME=="Georgia") %>%
  gather(key="Year", value="Population",
         POPESTIMATE2010, POPESTIMATE2011, POPESTIMATE2012,
         POPESTIMATE2013, POPESTIMATE2014, POPESTIMATE2015,
         POPESTIMATE2016, POPESTIMATE2017, POPESTIMATE2018) %>%
  select(Year, Population) %>%
  separate(Year, c(NA, "Year"), sep="POPESTIMATE",
         remove=TRUE, convert=TRUE)

view(df)

lmodel <- lm(Population ~ Year, df)

lmodel_grid <- data_grid(df, Year=seq_range(2010:2025, 16)) %>%
  add_predictions(lmodel, var="Population")

df <- add_residuals(df, lmodel, var="Residuals")

xticks <- seq_range(2010:2027, by=3)
yticks <- seq_range(0:11200000, by=200000)

model_plot <- ggplot(lmodel_grid, aes(x=Year, y=Population)) +
  geom_line(color="red") +
  geom_point(data=df, color="blue") +
  scale_x_continuous(breaks=xticks) +
  scale_y_continuous(breaks=yticks)

residual_plot <- ggplot(df, aes(x=Year, y=Residuals)) +
  geom_point()

model_plot
residual_plot
summary(lmodel)
predict(lmodel, data.frame(Year=2024))