# %% import
import numpy as np 
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["IPAexGothic"]
plt.rcParams["figure.dpi"] = 300
plt.rcParams["figure.facecolor"] = "white"

# %% loading data
data = np.loadtxt("precursor.csv", delimiter=",", skiprows=1)

time_hour = data[:, 0]
time_min = data[:, 1]
time_second = data[:, 2]


latitude = data[:, 3]
longitude = data[:, 4]

pressure = data[:, 5]
temperature = data[:, 6]
humidity = data[:, 7]

altitude = data[:, 8]

heading = data[:, 9]
roll = data[:, 10]
pitch = data[:, 11]

mag_x = data[:, 12]
mag_y = data[:, 13]
mag_z = data[:, 14]

gyro_x = data[:, 15]
gyro_y = data[:, 16]
gyro_z = data[:, 17]

accel_x = data[:, 18]
accel_y = data[:, 19]
accel_z = data[:, 20]

distance = data[:, 21]
direction = data[:, 22]

# %% calc relative time
time_mission = time_hour * 3600. + time_min * 60. + time_second
time_mission -= time_mission[0]

# %% plotting Time vs Altitude
fig, axes = plt.subplots()
axes.scatter(time_mission, altitude, s=5)
axes.set_xlabel("ミッション経過時間  [sec]")
axes.set_ylabel("高度   [m]")

fig.show()

# %% plotting Time vs Pressure and Temperature
fig, axes_press = plt.subplots()
axes_temp = axes_press.twinx()
axes_press.scatter(time_mission, pressure, s=5, color="orange")
axes_temp.scatter(time_mission, temperature, s=5, color="green")
axes_press.set_xlabel("ミッション経過時間  [sec]")
axes_press.set_ylabel("気圧   [hPa]")
axes_temp.set_ylabel("温度   [℃]")

fig.show()

# %% plotting Time vs Altitude and Pressure
fig, axes_altitude = plt.subplots()
axes_press = axes_altitude.twinx()
axes_altitude.scatter(time_mission, altitude, s=5)
axes_press.scatter(time_mission, pressure, s=5, color="orange")
axes_altitude.set_xlabel("ミッション経過時間  [sec]")
axes_altitude.set_ylabel("高度   [m]")
axes_press.set_ylabel("気圧   [hPa]")

# %%
fig, axes = plt.subplots(1, 2, figsize=(20, 8))

axes_altitude = axes[0].twinx()
axes[0].scatter(time_mission, pressure, s=5, color="orange")
axes_altitude.scatter(time_mission, altitude, s=5, color="blue")
axes[0].set_xlabel("ミッション経過時間  [sec]")
axes[0].set_ylabel("気圧   [hPa]")
axes_altitude.set_ylabel("高度   [m]")

axes_temp = axes[1].twinx()
axes[1].scatter(time_mission, pressure, s=5, color="orange")
axes_temp.scatter(time_mission, temperature, s=5, color="green")
axes[1].set_xlabel("ミッション経過時間  [sec]")
axes[1].set_ylabel("気圧   [hPa]")
axes_temp.set_ylabel("温度   [℃]")

fig.savefig("press-alitude&temp.png", bbox_inches="tight", pad_inches=0.05)
fig.show()

# %% more detail about the problem of pressure

fig, axes_press = plt.subplots()
axes_altitude = axes_press.twinx()
axes_press.scatter(time_mission[time_mission >= 300.],
             pressure[time_mission >= 300.],
             s=5,
             color="orange")
axes_altitude.scatter(time_mission[time_mission >= 300.],
             altitude[time_mission >= 300.],
             s=5,
             color="blue")
axes_altitude.set_xlabel("ミッション経過時間  [sec]")
axes_altitude.set_ylabel("高度   [m]")
axes_press.set_ylabel("気圧   [hPa]")

fig.savefig("press-altitude_more.png", bbox_inches="tight", pad_inches=0.05)
fig.show()

# %%
fig, axes = plt.subplots(3, 1, figsize=(10, 10))
axes[0].scatter(time_mission, accel_x, s=5, color="red")
axes[1].scatter(time_mission, accel_y, s=5, color="orange")
axes[2].scatter(time_mission, accel_z, s=5, color="green")

axes[2].set_xlabel("ミッション経過時間  [sec]")
axes[0].set_ylabel(r"$acc_x  \quad \rm{[m/s^2]}$")
axes[1].set_ylabel(r"$acc_y \quad \rm{[m/s^2]}$")
axes[2].set_ylabel(r"$acc_z \quad \rm{[m/s^2]}$")

fig.savefig("acc_xyz.png", bbox_inches="tight", pad_inches=0.05)
fig.show()

# %%
fig, axes = plt.subplots()
axes_altitude = axes.twinx()
axes_altitude.scatter(time_mission, altitude, s=5, color="blue")
axes.scatter(time_mission, accel_x, s=5, color="red")
axes.set_xlabel("ミッション経過時間  [sec]")
axes.set_ylabel(r"$acc_x  \quad \rm{[m/s^2]}$")
axes_altitude.set_ylabel("高度   [m]")

fig.savefig("acc_x-altitude.png")
fig.show()

# %%
fig, axes = plt.subplots()
axes_altitude = axes.twinx()
axes_altitude.scatter(time_mission, altitude, s=5, color="blue")
axes.scatter(time_mission, accel_z, s=5, color="green")
axes.set_xlabel("ミッション経過時間  [sec]")
axes.set_ylabel(r"$acc_z  \quad \rm{[m/s^2]}$")
axes_altitude.set_ylabel("高度   [m]")

fig.savefig("acc_z-altitude.png")
fig.show()

# %%
fig, axes_x = plt.subplots()
axes_z = axes_x.twinx()
axes_x.scatter(time_mission, accel_x, s=5, color="red")
axes_z.scatter(time_mission, accel_z, s=5, color="green")
axes_x.set_xlabel("ミッション経過時間  [sec]")
axes_x.set_ylabel(r"$acc_x  \quad \rm{[m/s^2]}$")
axes_z.set_ylabel(r"$acc_z  \quad \rm{[m/s^2]}$")

fig.savefig("acc_x-z.png")
fig.show()

# %%
fig, axes = plt.subplots(3, 1, figsize=(10, 10))
axes[0].scatter(time_mission, gyro_x, s=5, color="blue")
axes[1].scatter(time_mission, gyro_y, s=5, color="orange")
axes[2].scatter(time_mission, gyro_z, s=5, color="green")

axes[2].set_xlabel("ミッション経過時間  [sec]")
axes[0].set_ylabel(r"$gyro_x$" + "  [G]")
axes[1].set_ylabel(r"$gyro_y$" + "  [G]")
axes[2].set_ylabel(r"$gyro_z$" + "  [G]")

fig.savefig("gyro_xyz.png", bbox_inches="tight", pad_inches=0.05)
fig.show()

# %%
