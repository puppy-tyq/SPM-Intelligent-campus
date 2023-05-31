// index.js

Page({
  data: {
    places: ['图书馆', '操场', '食堂'],
    place: '图书馆',
    realtimeNum: 0,
    realtimeImage: ''
  },

  onPlaceChange: function(event) {
    const place = this.data.places[event.detail.value];
    wx.request({
      url: 'http://localhost:5000/get_realtime_info',
      method: 'POST',
      data: {place: place},
      success: (res) => {
        this.setData({
          place: place,
          realtimeNum: res.data.realtime_num,
          realtimeImage: res.data.realtime_image
        });
      },
      fail: (res) => {
        wx.showToast({
          title: '获取数据失败',
          icon: 'none'
        });
      }
    });
  }
});
