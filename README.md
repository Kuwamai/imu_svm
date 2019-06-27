# imu_svm

## Description
* IMUが取得したデータをsubscribeし、Support vector machineを用いたロボットの状態推定結果をpublishする
* Publishした推定結果がブラウザ上でplotされる
* 動画はこんな感じ
  * https://youtu.be/c9X_9prQ4ok
## Requirements
* Raspberry Pi3
* IMU
* Ubuntu16.04
* ROS kinetic
* rosbridge_server
## Installation
* 手頃なIMUをパブリッシュするパッケージを実行しておく
* 以下のコマンドで`/imu/data_raw`があることを確認

```
$ rostopic list 
/imu/data_raw
```

* このリポジトリをcloneする
* 以下のコマンドを実行

```
$ cd ~/catkin_ws/src/
$ git clone https://github.com/Kuwamai/imu_svm.git
$ cd ~/catkin_ws/
$ catkin_make
```

## Usage

* roslaunchで起動

```
$ roslaunch imu_svm imu_svm_server.launch
```

* ブラウザでアクセス

```
http://<ip_address>:8000
```

## License
This repository is licensed under the MIT license, see [LICENSE](./LICENSE).
