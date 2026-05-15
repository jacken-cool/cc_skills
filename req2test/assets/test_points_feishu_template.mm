<?xml version="1.0" encoding="utf-8"?>
<map>
  <node ID="root" TEXT="项目名称 / 需求名称">
    <node ID="e60ee694b40ad1ec562357bd9783122b" TEXT="测试范围" STYLE="bubble" POSITION="right">
      <node ID="9687c26030decc47e4a8371876b971b7" TEXT="范围内" STYLE="fork">
        <node ID="6ed0905b86773acf9cc88c3e847d0bca" TEXT="模块A" STYLE="fork"/>
        <node ID="5fe77b627c623730ea7b21601fdc6d4f" TEXT="模块B" STYLE="fork"/>
      </node>
      <node ID="d654b1218a17c356a5793bccc2bbd322" TEXT="范围外" STYLE="fork">
        <node ID="d898d58413de72089f95df2e36052c20" TEXT="非本次改造项" STYLE="fork"/>
      </node>
    </node>
    <node ID="faa05fd28f33ef240a058bbede683dc0" TEXT="核心业务链路" STYLE="bubble" POSITION="right">
      <node ID="900709f7cb233ecd44dd39fb1c5104ee" TEXT="配置端" STYLE="fork">
        <node ID="2c7991795245716a3817c5b53e169e7e" TEXT="字段新增" STYLE="fork"/>
        <node ID="4bdc86f98299203eda9facf8889cfbc3" TEXT="默认值" STYLE="fork"/>
        <node ID="b6c8656b7d15dfa01017d6c36d075aca" TEXT="校验规则" STYLE="fork"/>
      </node>
      <node ID="04f2c11509f4a565c35f5ed244fcdb1d" TEXT="同步链路" STYLE="fork">
        <node ID="ba46a63a757308995ffff9f5294a9a43" TEXT="新增同步" STYLE="fork"/>
        <node ID="b1cf45545eca754642a72da5d6f11157" TEXT="编辑同步" STYLE="fork"/>
        <node ID="a5870521713e14b089095830fdbfd536" TEXT="删除同步" STYLE="fork"/>
      </node>
      <node ID="d100c3e671f9b3626cae0c4e56757982" TEXT="展示端" STYLE="fork">
        <node ID="eca6f706f67bc33fbc29df2c2b8aef4c" TEXT="召回" STYLE="fork"/>
        <node ID="467546253b03471010213b956311c574" TEXT="过滤" STYLE="fork"/>
        <node ID="9eac12060260ef74c49d15c5b361f2b7" TEXT="排序" STYLE="fork"/>
        <node ID="428656b1761bacf18ab25a2544192a35" TEXT="跳转" STYLE="fork"/>
      </node>
    </node>
    <node ID="74b495309056bdbc7245305c6beb1d42" TEXT="模块测试点" STYLE="bubble" POSITION="left">
      <node ID="427673e65ee37b9c8f78398489d1e4eb" TEXT="APP / 前端" STYLE="fork">
        <node ID="59dbf0d934b33760ead0b5f18c24a2f2" TEXT="tab 展示" STYLE="fork">
          <node ID="64ef2f76983192b710d4df5448ada8f0" TEXT="默认态" STYLE="fork"/>
          <node ID="87e2e8e4fb65d7f256d2baecd457adf0" TEXT="切换态" STYLE="fork"/>
        </node>
        <node ID="a601db96abe6e74667e2fc4de55bb200" TEXT="搜索结果" STYLE="fork">
          <node ID="e0dae50c19d12d26d91ac269c89e3c15" TEXT="名称召回" STYLE="fork"/>
          <node ID="11525cc4beff1b6ddcdca2734e487b7b" TEXT="描述仅展示" STYLE="fork"/>
          <node ID="1e0435ab47624d6f1fbc2ad750b5126c" TEXT="icon 兜底" STYLE="fork"/>
        </node>
        <node ID="e0d5da87c290503fb43280e69e7a2329" TEXT="异常态" STYLE="fork">
          <node ID="4d2c6b43a5108c3e9ece0554048e1c9c" TEXT="无结果" STYLE="fork"/>
          <node ID="c557ca1009b1775eee51d5f0556cca9b" TEXT="网络异常" STYLE="fork"/>
          <node ID="78606672d82d01610e1fb6c734999ef9" TEXT="服务异常" STYLE="fork"/>
        </node>
      </node>
      <node ID="10d9e9a14e93c27eaeec53a632bf8db8" TEXT="配置后台" STYLE="fork">
        <node ID="4d2c6b43a5108c3e9ece0554048e1c9c" TEXT="必填校验" STYLE="fork"/>
        <node ID="c557ca1009b1775eee51d5f0556cca9b" TEXT="长度校验" STYLE="fork"/>
        <node ID="78606672d82d01610e1fb6c734999ef9" TEXT="开关校验" STYLE="fork"/>
        <node ID="aa117f1f8a7e151373f87022fcbfbc60" TEXT="回填校验" STYLE="fork"/>
      </node>
      <node ID="53f4c3d10ed6d1767132e72fef780feb" TEXT="运营后台" STYLE="fork">
        <node ID="fc800f16a7522864faf591049340a783" TEXT="tab 管理" STYLE="fork"/>
        <node ID="39f6e601b6c57c3f14dcfe2cf9d29686" TEXT="菜单管理" STYLE="fork"/>
        <node ID="caf7ea3edadb3343f44fd3139d7bcb07" TEXT="有效期" STYLE="fork"/>
        <node ID="d1bc92bfa4b66f1f0df463d033f00a96" TEXT="人群" STYLE="fork"/>
      </node>
    </node>
    <node ID="f53f7153a7775abeffa41b4ea3f56f09" TEXT="高优先级场景" STYLE="bubble" POSITION="left">
      <node ID="87f9c5263cb80fe25438c711d8e93179" TEXT="P0" STYLE="fork">
        <node ID="7a0cb117f3a11bda08bf3c5df8ecc1ec" TEXT="主流程闭环" STYLE="fork"/>
        <node ID="27d0f3807739d7332c5cf5111615f303" TEXT="权限过滤" STYLE="fork"/>
        <node ID="8a94bc829baa87f91489e878ca22933a" TEXT="有效期过滤" STYLE="fork"/>
      </node>
      <node ID="7280636e86140750deba66c84a1d15e8" TEXT="P1" STYLE="fork">
        <node ID="ba0b4ceac1850bfe471fab795e8d4eb6" TEXT="边界值" STYLE="fork"/>
        <node ID="9abb7a78ffd3a2a97a12778f995c5e22" TEXT="输入校验" STYLE="fork"/>
        <node ID="ee12f9577bb6262cbbd83ab080393985" TEXT="异常补偿" STYLE="fork"/>
      </node>
      <node ID="c4cb1e545afe35d4338095674be188eb" TEXT="P2" STYLE="fork">
        <node ID="332c769bb2b0b88a04c2afdebe7a594f" TEXT="回归稳定性" STYLE="fork"/>
      </node>
    </node>
    <node ID="d446d8be3cde9529e565b04118c7e93e" TEXT="待确认项" STYLE="bubble" POSITION="right">
      <node ID="81b9e464fe1af79d031b63d043ad62d2" TEXT="计数口径" STYLE="fork"/>
      <node ID="6917142e60162b8e3bf04d9bb6a3789a" TEXT="冲突优先级" STYLE="fork"/>
      <node ID="70c0b12f2930e6d72ec1fe2339fedeb2" TEXT="刷新时机" STYLE="fork"/>
    </node>
  </node>
</map>
