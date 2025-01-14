#include <fstream>
#include <locale>
#include <codecvt>
#include "../include/Compose.h"
#include "../include/Factory.h"

class JsonExplorer
{
private:
    Container root;
    shared_ptr<TopAbstractFactory> factory;
    shared_ptr<ProductFactory> decorationFactory;
    void getFileContent(vector<string> &fileContent, string json_file)
    {
        std::ifstream file(json_file);
        if (!file.is_open())
        {
            std::cerr << "Error opening file" << std::endl;
            return;
        }

        std::string line;
        while (std::getline(file, line))
        {
            line.erase(0, line.find_first_not_of(" \t\n\r\f\v"));
            line.erase(line.find_last_not_of(" \t\n\r\f\v") + 1);
            fileContent.push_back(line);
        }

        file.close();
    }

public:
    JsonExplorer(string style, string icon_family)
    {
    }
    void _load(string json_file)
    {
        vector<string> fileContent;
        getFileContent(fileContent, json_file);
        int index = 1;
        fileContent.pop_back();
        root.addContainerOrLeaf(index, fileContent);
    }

    // 设置客户自定义工厂
    void setFactory(shared_ptr<TopAbstractFactory> factory)
    {
        this->factory = move(factory);
    }

    // 建立图标和风格工厂
    shared_ptr<ProductFactory> createIconFactory()
    {
        return factory->createIconFactory();
    }
    shared_ptr<ProductFactory> createStyleFactory()
    {
        return factory->createStyleFactory();
    }

    // 设置装饰工厂
    void setDecorationFactory(shared_ptr<ProductFactory> decorationFactory)
    {
        this->decorationFactory = decorationFactory;
    }

    shared_ptr<Decoration> createIcon(string middleNode, string leafNode)
    {
        return decorationFactory->createIcon(middleNode, leafNode);
    }
    shared_ptr<Decoration> createStyle(string style, vector<string> &format)
    {
        return decorationFactory->createStyle(style, format);
    }

    void draw(Icon &icon, Style &style) const
    {
        outBuffer.clear();
        root.draw(icon, style, false);

        int len = 0;
        for (auto &x : outBuffer)
        {
            // cout<<x.size()<<endl;
            len = max(len, (int)x.size());
        }
        int additional = 6;

        for (int i = 0; i < outBuffer.size(); ++i)
        {
            string &x = outBuffer[i];
            string output = x;

            int diff = (len-x.size());

            for (int i = 0; i < diff + additional; ++i)
            {
                output += style.getFormat(11);
            }
            if (i == 0)
            {
                output += style.getFormat(7);
            }
            else if (i == outBuffer.size() - 1)
            {
                for (int i = 0; i < 6; ++i)
                {
                    output+= style.getFormat(11);
                }
                output += style.getFormat(9);
            }
            else
            {
                output += style.getFormat(1);
            }
            cout << output << endl;
        }
    }
};

int main(int argc, char *argv[])
{
    std::string json_file = "input/input.json";
    std::string style = "tree";
    std::string icon_family = "default";
    if (argc != 7)
    {
        std::cerr << "Usage: " << argv[0] << " -f <json file> -s <style> -i <icon family>" << std::endl;
        return 1;
    }

    for (int i = 1; i < argc; i += 2)
    {
        std::string arg = argv[i];
        if (arg == "-f")
        {
            json_file = argv[i + 1];
        }
        else if (arg == "-s")
        {
            style = argv[i + 1];
        }
        else if (arg == "-i")
        {
            icon_family = argv[i + 1];
        }
        else
        {
            std::cerr << "Unknown argument: " << arg << std::endl;
            return 1;
        }
    }

    std::cout << "JSON file: " << json_file << " , ";
    std::cout << "Style: " << style << " , ";
    std::cout << "Icon family: " << icon_family << std::endl;

    setlocale(LC_ALL, "chs");
    std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;

    // 创建JsonExplorer对象
    JsonExplorer explorer(style, icon_family);

    // 加载json文件
    explorer._load(json_file);

    // 建立客户工厂
    MyFactory factory;
    explorer.setFactory(make_shared<MyFactory>(factory));

    // 建立装饰工厂
    shared_ptr<ProductFactory> iconFactory = explorer.createIconFactory();
    shared_ptr<ProductFactory> styleFactory = explorer.createStyleFactory();

    // 设置装饰工厂
    explorer.setDecorationFactory(iconFactory);
    shared_ptr<Decoration> myIcon = nullptr; 
    vector<string> icons(2);
    if(icon_family == "default"){
        icons[0] = " ";
        icons[1] = " ";
    }
    else if(icon_family == "poker"){
        icons[0] = converter.to_bytes(wstring(L"♢"));
        icons[1] = converter.to_bytes(wstring(L"♤"));
    }
    else{
        cout<<"Unknown icon family"<<endl;
        return 1;
    }
    myIcon = explorer.createIcon(icons[0], icons[1]);
    vector<string> format;
    shared_ptr<Decoration> myStyle = nullptr;
    explorer.setDecorationFactory(styleFactory);
    if(style == "tree"){
        format = {"└", " ", "├", "|", "─", "└", "├", " ", " ", " ", " ", " "};
    }
    else if (style == "rectangle"){
        format = {"├", "┤", "├", "|", "─", "┴", "┌", "┐", "└", "┘", "|", "─"};
    }
    else{
        cout<<"Unknown style"<<endl;
        return 1;
    }
    myStyle = explorer.createStyle(style, format);
    printf("----------------------------------------\n");
    Icon* changeIcon = dynamic_cast<Icon*>(myIcon.get());
    Style* changeStyle = dynamic_cast<Style*>(myStyle.get());
    explorer.draw(*changeIcon, *changeStyle);

    return 0;
}
