import ast

from kt_base import CommonUtils
from matplotlib import pyplot as plt
from kt_text.Config import Config

class LineChartUtils:
    def __init__(self, param):
        self.title_name = param.get("titleName")
        if self.title_name is None:
            self.title_name = ""
        self.title_color = param.get("titleColor")
        if self.title_color is None:
            self.title_color = "#EE3B3B"
        self.title_font_size = param.get("titleFontSize")
        if self.title_font_size is None:
            self.title_font_size = 16

        self.x_label_name = param.get("xLabelName")
        if self.x_label_name is None:
            self.x_label_name = "X轴"
        self.x_label_color = param.get("xLabelColor")
        if self.x_label_color is None:
            self.x_label_color = "#333333"

        self.y_label_name = param.get("yLabelName")
        if self.y_label_name is None:
            self.y_label_name = "Y轴"
        self.y_label_color = param.get("yLabelColor")
        if self.y_label_color is None:
            self.y_label_color = "#333333"

        self.x_key = param.get("xKey")
        if self.x_key is None:
            raise Exception("X轴取数标识：xKey，不能为空")

        self.y_keys = param.get("yKeys")
        if self.y_keys is None:
            raise Exception("Y轴取数标识：yKeys，不能为空")
        self.y_keys = ast.literal_eval("{" + self.y_keys + "}")

        self.data = param.get("data")
        if self.data is None:
            raise Exception("用于生成折线图的数据：data，不能为空")
        if isinstance(self.data, str):
            self.data = ast.literal_eval(self.data)

    def __str__(self):
        fields = vars(self)
        field_str = ', '.join([f"{k}={v}" for k, v in fields.items()])
        return f"LineChartUtils({field_str})"

    def save_img(self):
        file_name = CommonUtils.generate_uuid() + ".png";
        plt.savefig(Config.BASE_PATH + file_name)
        return file_name

    def generate_line_chart(self):
        x = []
        grouped_data = {key: [] for key in self.y_keys}
        print(grouped_data)
        for item in self.data:
            x.append(item.get(self.x_key))
            for key in self.y_keys:
                grouped_data[key].append(item[key])
        print(grouped_data)
        plt.rcParams['font.sans-serif'] = ['SimSun']  # 使用微软雅黑
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

        fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=200)
        fig.patch.set_facecolor('#FFFFFF')
        # 设置图表内容与画布边缘的边距（单位：画布宽高的比例，范围 0~1）
        plt.subplots_adjust(
            left=0.05,  # 左边距（默认 0.125）
            right=0.95,  # 右边距（默认 0.9）
            bottom=0.1,  # 下边距（默认 0.11）
            top=0.9  # 上边距（默认 0.88）
        )
        ax.set_facecolor('#FFFFFF')
        for spine in ax.spines.values():
            spine.set_color('#d7d7d7')

        for key in self.y_keys:
            ax.plot(x, grouped_data[key], label=key, color=self.y_keys[key], linestyle='-', linewidth=0.85, alpha=0.5)

        # ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=12, frameon=False)
        """
        legend = ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.3), ncol=8,
                           frameon=False, handlelength=1, handletextpad=0.6, fontsize=10)

        if self.title_name != '':
            ax.set_title(self.title_name, color=self.title_color, fontsize=self.title_font_size, fontweight='bold', pad=15)  # 设置标题颜色
        ax.set_xlabel(self.x_label_name, color=self.x_label_color, fontsize=14, labelpad=10)  # 设置X轴标签颜色
        ax.set_ylabel(self.y_label_name, color=self.y_label_color, fontsize=14, labelpad=10)  # 设置Y轴标签颜色
        """
        # 调整底部边距防止标签被裁剪
        plt.subplots_adjust(bottom=0.1)

        for spine in ['left', 'bottom']:
            ax.spines[spine].set_visible(True)
            ax.spines[spine].set_color('#d7d7d7')  # 目标颜色
            ax.spines[spine].set_linewidth(0.5)

        for spine in ['right', 'top']:
            ax.spines[spine].set_visible(True)
            ax.spines[spine].set_color('#d7d7d7')  # 目标颜色
            ax.spines[spine].set_linewidth(0)

        # 刻度设置
        # 2. 调整刻度线及标签样式
        ax.tick_params(
            direction='out',
            length=4,
            width=0,
            color='#d7d7d7',
            pad=0,
            labelcolor='#2F5597'
        )
        ax.tick_params(axis="both", labelsize=8, colors="#777777")
        ax.grid(True, axis='y', linestyle="-", color="#d7d7d7", linewidth=0.5, alpha=0.5)
        # 添加图例（左上角）
        ax.legend(
            loc='upper left',
            bbox_to_anchor=(0, 1.02),
            ncol=3,
            frameon=False,
            borderaxespad=-1.5,
            # ==== 新增参数 ====
            prop={'size': 6},  # 字体大小
            labelcolor='#777777'  # 字体颜色
        )

       # plt.show()
        return self.save_img()



